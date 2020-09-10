#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

TEMPLATE = """
import sys
import os
import importlib
import random
import pandas as pd
from datetime import datetime, timedelta
import pathlib
from collections import defaultdict
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.configuration import get_airflow_home
from airflow.utils.log.logging_mixin import LoggingMixin
sys.path.append(os.path.dirname(get_airflow_home()))
from system.cloudtdms import providers
from system.dags import get_providers_home
from system.dags import get_output_data_home


dag = DAG(
dag_id={{ "'"~data.dag_id|string~"'" }},
        schedule_interval={{"'@"~data.frequency~"'"}},
        catchup=False,
        default_args={
            'owner': 'CloudTDMS',
            'depends_on_past': False,
            'start_date': datetime(2020, 7, 8),
            'retries': 1,
            'retry_delay': timedelta(minutes=1)
        },
        params={
            'stream': {{ data.stream }},
            'attributes': {{ data.attributes }}
        }
)


def generate_iterator(data_frame, methods,args_array):
    number = dag.params.get('stream').get('number')
    for fcn, name in methods:
        func_name = fcn.__name__
        arg = args_array.get(func_name)
        if arg is None:
            result = fcn(data_frame, number)
        else:
            result = fcn(data_frame,number, arg)
        # data_frame[name] = pd.Series(result) 
        

def data_generator():
    meta_data = providers.get_active_meta_data()
    stream = dag.params.get('stream')
    locale=dag.params.get('stream').get('locale')
    schema = stream['schema']
    attributes = dag.params.get('attributes')
    nrows = stream['number']
    ncols = sum([len(f) for f in attributes.values()])
    columns = []
    labels = [columns.extend(f) for f in attributes.values()]
    data_frame = pd.DataFrame(pd.np.zeros((nrows, ncols))*pd.np.nan, columns=[v + str(columns[:i].count(v)) if columns.count(v) > 1 and columns[:i].count(v) != 0 else v for i, v in enumerate(columns)])    
    
    for attrib in attributes:
        if attrib in meta_data['data_files']:
            try:
                df = pd.read_csv(list(pathlib.Path(get_providers_home()).rglob(f"{attrib}.csv")).pop(0), usecols=[column for (field_name, column) in attributes[attrib]])
            except (FileNotFoundError, IndexError):
                df = pd.read_csv(f"{os.path.dirname(get_airflow_home())}/user-data/{attrib}.csv", usecols=[column for (field_name, column) in attributes[attrib]])

            df_temp = pd.DataFrame(index=range(nrows), columns=[column for (field_name, column) in attributes[attrib]])
            for i in range(nrows):
                df_temp.iloc[i] = df.iloc[random.randrange(len(df))]
                            
            data_frame[[column for (field_name, column) in attributes[attrib]]] = df_temp[[column for (field_name, column) in attributes[attrib]]]
        elif attrib in meta_data['code_files']:
            mod = importlib.import_module(f"system.cloudtdms.providers.{attrib}")
            args_array={f"{f['field_name']}-$-{f['type'].split('.')[1]}": {k: v for k, v in f.items() if k not in ('field_name', 'type')} for f in schema if f.get('type').startswith(attrib)}
            try:
                args_array['locale']=locale
                _all = getattr(mod, attrib)                
                _all(data_frame, nrows, args_array)
            except AttributeError:
                # args_array={f['type'].split('.')[1]: {k: v for k, v in f.items() if k not in ('field_name', 'type')} for f in schema if len(f) > 2}
                methods = [(getattr(mod, m), m) for m in attributes[attrib]]
                generate_iterator(data_frame, methods,args_array)
    
    file_name = f"{stream['title']}_{datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')}.csv"
    try:
        data_frame.to_csv(f"{get_output_data_home()}/{stream['title']}/{file_name}", index=False)
    except FileNotFoundError:
        os.makedirs(f"{get_output_data_home()}/{stream['title']}")
        data_frame.to_csv(f"{get_output_data_home()}/{stream['title']}/{file_name}", index=False)
    
start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id="end", dag=dag)
stream = PythonOperator(task_id="GenerateStream", python_callable=data_generator, dag=dag)

start >> stream >> end

"""

# --------------------------------- Discovery ----------------------------------------

DISCOVER = """
import sys
import os
import yaml
import email, smtplib, ssl
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.configuration import get_airflow_home
from airflow.utils.log.logging_mixin import LoggingMixin
sys.path.append(os.path.dirname(get_airflow_home()))
from system.dags import get_user_data_home, get_cloudtdms_home, get_config_default_path, get_reports_home
from system.cloudtdms.discovery import discover
from pandas_profiling import ProfileReport
from system.cloudtdms.utils.pii_report import PIIReport

dag = DAG(
    dag_id={{ "'"~data.dag_id|string~"'" }},
    schedule_interval={{"'@"~data.frequency~"'"}},
    catchup=False,
    default_args={
        'owner': 'CloudTDMS',
        'depends_on_past': False,
        'start_date': datetime(2020, 7, 8),
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
    },
    params={
       'data_file' : {{ "'"~data.data_file|string~"'" }}
    }
)


def generate_eda_profile():
    df = pd.read_csv(f"{get_user_data_home()}/{dag.params.get('data_file')}.csv")
    columns = list(map(lambda x : str(x).lower().replace(' ', '_'), df.columns))
    df.columns = columns
    profile = ProfileReport(
        df, title=f"Exploratory Data Analysis of the data-set {dag.params.get('data_file')}", explorative=True
    )
    path = f"{get_reports_home()}/{dag.params.get('data_file')}"
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    profile.to_file(f"{path}/profiling_{dag.params.get('data_file')}.html")

def generate_sensitive_data_profile():
    df = pd.read_csv(f"{get_user_data_home()}/{dag.params.get('data_file')}.csv")
    columns = list(map(lambda x : str(x).lower().replace(' ', '_'), df.columns))
    df.columns = columns
    profile = PIIReport(
        df,filename=dag.params.get('data_file'), title=f"Sensitive Data Discovery Report of the data-set {dag.params.get('data_file')}", explorative=True
    )
    path = f"{get_reports_home()}/{dag.params.get('data_file')}"
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    profile.to_file(f"{path}/pii_{dag.params.get('data_file')}.html")

def email_reports():
    # Get config_default.yaml
    file = open(get_config_default_path())
    config = yaml.load(file, Loader=yaml.FullLoader)
    email = config["email"]
    subject = "Data Profile"
    body = "This is an email with attachment sent from CloudTDMS"
    sender_email = email["username"]
    receiver_email = email["to"]
    password = email["password"]

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    path = f"{get_reports_home()}/{dag.params.get('data_file')}"
    
    for file in os.listdir(path):
        with open(f"{path}/{file}", "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
    
        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)
    
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file}",
        )
    
        # Add attachment to message and convert message to string
        message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(email["smtp_host"], email["smtp_port"], context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        
        
start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id="end", dag=dag)
eda_stream = PythonOperator(task_id="ExploratoryDataProfiling", python_callable=generate_eda_profile, dag=dag)
send_email = PythonOperator(task_id="EmailReports", python_callable=email_reports, dag=dag)
sensitive_data_profile = PythonOperator(task_id="SensitiveDataDiscovery", python_callable=generate_sensitive_data_profile, dag=dag)
start >> [eda_stream, sensitive_data_profile]>> send_email >> end


"""