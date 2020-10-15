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
from system.dags import get_user_data_home


{% if 'mysql' in data.destination %} 
from system.cloudtdms.extras.mysql import mysql_upload 
{% endif %}

{% if 'mysql' in data.source %} 
from system.cloudtdms.extras.mysql import mysql_download 
{% endif %}

{% if 'servicenow' in data.destination %} 
from system.cloudtdms.extras.servicenow import service_now_upload 
{% endif %}

{% if 'servicenow' in data.source %} 
from system.cloudtdms.extras.servicenow import service_now_download 
{% endif %}

{% if 's3' in data.destination %} 
from system.cloudtdms.extras.amazons3 import s3_upload 
{% endif %}

{% if 's3' in data.source %} 
from system.cloudtdms.extras.amazons3 import s3_download 
{% endif %}


dag = DAG(
dag_id={{ "'"~data.dag_id|string~"'" }},
        schedule_interval={{"'@"~data.frequency~"'"}},
        catchup=False,
        default_args={
            'owner': "{{ data.owner | string }}",
            'depends_on_past': False,
            'start_date': datetime(2020, 7, 8),
            'retries': 1,
            'retry_delay': timedelta(minutes=1)
        },
        params={
            'stream': {{ data.stream }},
            'source': {{ data.source }},
            'attributes': {{ data.attributes }},
            'destination': {{ data.destination }}
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
        

def data_generator(**kwargs):
    stream = dag.params.get('stream')
    meta_data = providers.get_active_meta_data()
    stream['format'] = 'csv'

    # check 'source' attribute is present
    file_name = f"{stream['title']}_{str(kwargs['execution_date'])[:19].replace('-','_').replace(':','_')}.csv"
    source = f'{get_user_data_home()}/{file_name}' if 'source' in stream else None

    # columns in data-file
    all_columns = []
    if source is not None:
        try:
            all_columns = pd.read_csv(source, nrows=1).columns
        except FileNotFoundError:
            LoggingMixin().log.error(f'ValueError: File {source} not found')

    # get columns to delete
    delete = stream['delete'] if 'delete' in stream else []

    all_columns=[f for f in all_columns if f not in delete]

    # check 'schema' attribute is present
    schema = stream['schema'] if 'schema' in stream else []

    # check 'substitute' attribute is present along with 'source'
    if 'substitute' in stream and source is not None:
        substitutions = []
        for k, v in stream['substitute'].items():
            v['field_name'] = k
            substitutions.append(v)

        schema += substitutions

    # check 'encrypt' attribute is present along with 'source'

    if 'encrypt' in stream and source is not None:
        encryption = [{"field_name": v, "type": "advanced.custom_file", "name": file_name, "column": v,
                       "ignore_headers": "no", "encrypt": {"type": stream['encrypt']["type"], "key": stream['encrypt']["encryption_key"]}}
                      for v in stream['encrypt']['columns'] if v in all_columns]
        schema += encryption

    # check 'mask_out' attribute is present along with 'source'

    if 'mask_out' in stream and source is not None:
        mask_outs = [{"field_name": k, "type": "advanced.custom_file", "name": file_name,
                      "column": k, "ignore_headers": "no", "mask_out": {"with": v['with'], "characters": v['characters'], "from": v["from"]}}
                     for k, v in stream['mask_out'].items() if k in all_columns]
        schema += mask_outs

    # check 'shuffle' attribute is present along with 'source'

    if 'shuffle' in stream and source is not None:

        shuffle = [{"field_name": v, "type": "advanced.custom_file", "name": file_name, "column": v,
                    "ignore_headers": "no", "shuffle": True} for v in stream['shuffle'] if v in all_columns]
        schema += shuffle

    # check 'nullying' attribute is present along with 'source'

    if 'nullying' in stream and source is not None:

        nullify = [{"field_name": v, "type": "advanced.custom_file", "name": file_name, "column": v,
                    "ignore_headers": "no", "set_null": True} for v in stream['nullying'] if v in all_columns]
        schema += nullify

    if source is not None:
        schema_fields = [f['field_name'] for f in schema]
        remaining_fields = list(set(all_columns) - set(schema_fields))
        remaining = [{"field_name": v, "type": "advanced.custom_file", "name": file_name, "column": v,
                        "ignore_headers": "no"} for v in remaining_fields if v in all_columns]
        schema += remaining
    
    stream['schema'] = schema

    if not schema:
        LoggingMixin().log.error(f"AttributeError: attribute `schema` not found or is empty in {name}.py")
        # continue

    # Remove Duplicates In Schema
    new_schema = {}
    for s in schema:
        new_schema[s['field_name']] = s
    schema = list(new_schema.values())

    for col in [f['field_name'] for f in schema]:
        if col not in all_columns:
            all_columns.append(col)

    stream['original_order_of_columns'] = all_columns

    schema.sort(reverse=True, key=lambda x: x['type'].split('.')[1])

    attributes = {}
    for scheme in schema:
        data, column = scheme['type'].split('.')
        if data in meta_data['data_files']:
            if column in meta_data['meta-headers'][data]:
                if data not in attributes:
                    attributes[data] = [column]
                else:
                    attributes[data].append(column)
            else:
                raise AirflowException(f"TypeError: no data available for type {column} ")
        elif data in meta_data['code_files']:
            if column in meta_data['meta-functions'][data]:
                if data not in attributes:
                    attributes[data] = [column]
                else:
                    attributes[data].append(column)
            else:
                raise AirflowException(f"TypeError: no data available for type {column} ")
        else:
            raise AirflowException(f"IOError: no data file found {data}.csv ")
            
    locale=dag.params.get('stream').get('locale')

    nrows = int(stream['number'])
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
    file_name = f"{stream['title']}_{str(kwargs['execution_date'])[:19].replace('-','_').replace(':','_')}.csv"
    try:
        data_frame = data_frame[stream['original_order_of_columns']]
        data_frame.to_csv(f"{get_output_data_home()}/{dag.owner}/{stream['title']}/{file_name}", index=False)
    except FileNotFoundError:
        os.makedirs(f"{get_output_data_home()}/{dag.owner}/{stream['title']}")
        data_frame.to_csv(f"{get_output_data_home()}/{dag.owner}/{stream['title']}/{file_name}", index=False)
        
   
start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id="end", dag=dag)
stream = PythonOperator(task_id="GenerateStream", python_callable=data_generator, op_kwargs={'execution_date': {%raw%}"{{ execution_date }}"{%endraw%} }, dag=dag)

{% if data.source.mysql | length == 0 and data.source.s3 | length == 0 and data.source.servicenow | length == 0%}
start >> stream
{% endif %}


{% if 'mysql' in data.source and data.source.mysql %}

{% for connection in data.source.mysql %}

# Initialize task for MySQL db Extract {{connection.connection}} and table {{connection.table}}
{{connection.connection}}_d_kwargs = {} 
{{connection.connection}}_d_kwargs['execution_date'] = {% raw %}"{{ execution_date }}"{% endraw %}
{{connection.connection}}_d_kwargs['databases']=dag.params.get('destination').get('mysql')
{{connection.connection}}_d_kwargs['folder_title']=dag.params['stream']['title'] # for reading file
{{connection.connection}}_d_kwargs['prefix'] = dag.params.get('stream').get('title')
{{connection.connection}}_d_mysql = PythonOperator(task_id="ExtractMySQL_{{connection.connection}}_{{connection.table}}", python_callable=mysql_download, op_kwargs={{connection.connection}}_d_kwargs, dag=dag)
{{connection.connection}}_d_mysql.set_upstream(start)
{{connection.connection}}_d_mysql.set_downstream(stream)

{% endfor %}

{% endif %}


{% if 'servicenow' in data.source and data.source.servicenow %}

{% for connection in data.source.servicenow %}
# Initialize task for ServiceNow Instance Extract {{connection.connection}} and table {{connection.table}}
{{connection.connection}}_d_op_kwargs = {} 
{{connection.connection}}_d_op_kwargs['execution_date'] = {% raw %}"{{ execution_date }}"{% endraw %}
{{connection.connection}}_d_op_kwargs['table_name'] = "{{connection.table}}"
{{connection.connection}}_d_op_kwargs['instance'] = "{{connection.connection}}"
{{connection.connection}}_d_op_kwargs['prefix'] = f"{dag.owner}/{dag.params.get('stream').get('title')}"
{{connection.connection}}_d_op_kwargs['limit'] = "{{connection.limit}}"
{{connection.connection}} = PythonOperator(task_id="ExtractServiceNow_{{ connection.connection }}_{{ connection.table }}", python_callable=service_now_download, op_kwargs={{connection.connection}}_d_op_kwargs, dag=dag)
{{connection.connection}}.set_upstream(start)
{{connection.connection}}.set_downstream(stream)

{% endfor %}


{% if 's3' in data.source  and data.source.s3%}

{% for connection in data.source.s3 %}
# Initialize task for Amazon S3 {{connection.connection}} and bucket {{connection.bucket}}
{{connection.connection}}_s3 = PythonOperator(task_id="AmazonS3_{{connection.connection}}_{{connection.bucket}}", python_callable=s3_download, dag=dag)
{{connection.connection}}_s3.set_upstream(start)
{{connection.connection}}_s3.set_downstream(stream)
{% endfor %}

{% endif %}

{% endif %}

{% if 's3' in data.destination  and data.destination.s3%}

{% for connection in data.destination.s3 %}
# Initialize task for Amazon S3 {{connection.connection}} and bucket {{connection.bucket}}
{{connection.connection}}_s3 = PythonOperator(task_id="AmazonS3_{{connection.connection}}", python_callable=s3_upload, dag=dag)
{{connection.connection}}_s3.set_upstream(stream)
{{connection.connection}}_s3.set_downstream(end)
{% endfor %}

{% endif %}


{% if 'mysql' in data.destination and data.destination.mysql %}

{% for connection in data.destination.mysql %}

# Initialize task for MySQL db {{connection.connection}} and table {{connection.table}}
{{connection.connection}}_kwargs = {} 
{{connection.connection}}_kwargs['execution_date'] = {% raw %}"{{ execution_date }}"{% endraw %}
{{connection.connection}}_kwargs['databases']=dag.params.get('destination').get('mysql')
{{connection.connection}}_kwargs['folder_title']=dag.params['stream']['title'] # for reading file
{{connection.connection}}_kwargs['prefix'] = dag.params.get('stream').get('title')
{{connection.connection}}_mysql = PythonOperator(task_id="MySQL_{{connection.connection}}", python_callable=mysql_upload, op_kwargs={{connection.connection}}_kwargs, dag=dag)
{{connection.connection}}_mysql.set_upstream(stream)
{{connection.connection}}_mysql.set_downstream(end)

{% endfor %}

{% endif %}

{% if 'servicenow' in data.destination and data.destination.servicenow %}

{% for connection in data.destination.servicenow %}
# Initialize task for ServiceNow Instance {{connection.connection}} and table {{connection.table}}
{{connection.connection}}_op_kwargs = {} 
{{connection.connection}}_op_kwargs['execution_date'] = {% raw %}"{{ execution_date }}"{% endraw %}
{{connection.connection}}_op_kwargs['table_name'] = "{{connection.table}}"
{{connection.connection}}_op_kwargs['instance'] = "{{connection.connection}}"
{{connection.connection}}_op_kwargs['prefix'] = f"{dag.owner}/{dag.params.get('stream').get('title')}"
{{connection.connection}} = PythonOperator(task_id="ServiceNow_{{ connection.connection }}_{{ connection.table }}", python_callable=service_now_upload, op_kwargs={{connection.connection}}_op_kwargs, dag=dag)
{{connection.connection}}.set_upstream(stream)
{{connection.connection}}.set_downstream(end)

{% endfor %}

{% endif %}

{% if 'mysql' not in data.destination  and 'servicenow' not in data.destination and 's3' not in data.destination %}
start >> stream >> end
{% elif data.destination.mysql | length == 0 and data.destination.s3 | length == 0 and data.destination.servicenow | length == 0%}
start >> stream >> end
{% endif %}



"""

# --------------------------------- Discovery ----------------------------------------

DISCOVER = """
import sys
import os
from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.configuration import get_airflow_home
from airflow.utils.log.logging_mixin import LoggingMixin
sys.path.append(os.path.dirname(get_airflow_home()))
from system.dags import get_profiling_data_home, get_cloudtdms_home, get_config_default_path, get_reports_home
from system.cloudtdms.discovery import discover
from pandas_profiling import ProfileReport
from system.cloudtdms.utils.pii_report import PIIReport
from system.cloudtdms.utils.smtp_email import SMTPEmail

dag = DAG(
    dag_id={{ "'"~data.dag_id|string~"'" }},
    schedule_interval={{"'@"~data.frequency~"'"}},
    catchup=False,
    default_args={
        'owner': "{{ data.owner | string }}",
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
    if dag.owner == 'CloudTDMS':
        df = pd.read_csv(f"{get_profiling_data_home()}/{dag.params.get('data_file')}.csv")
        path = f"{get_reports_home()}/{dag.params.get('data_file')}"
    else:
        df = pd.read_csv(f"{get_profiling_data_home()}/{dag.owner}/{dag.params.get('data_file')}.csv")
        path = f"{get_reports_home()}/{dag.owner}/{dag.params.get('data_file')}"
    
    profile = ProfileReport(
        df.loc[0:10000], title=f"CloudTDMS Exploratory Data Analysis", explorative=True
    )
    
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    profile.to_file(f"{path}/profiling_{dag.params.get('data_file')}.html")

def generate_sensitive_data_profile():
    if dag.owner == 'CloudTDMS':
        df = pd.read_csv(f"{get_profiling_data_home()}/{dag.params.get('data_file')}.csv")
        path = f"{get_reports_home()}/{dag.params.get('data_file')}"
    else:
        df = pd.read_csv(f"{get_profiling_data_home()}/{dag.owner}/{dag.params.get('data_file')}.csv")
        path = f"{get_reports_home()}/{dag.owner}/{dag.params.get('data_file')}"
        
    column_mapping = {str(f).lower().replace(' ', '_'):f for f in df.columns}
    columns =  list(column_mapping.keys()) #list(map(lambda x : str(x).lower().replace(' ', '_'), df.columns))
    df.columns = columns
    profile = PIIReport(
        df.loc[0:10000], filename=dag.params.get('data_file'), title=f"CloudTDMS Sensitive Data Report", explorative=True,
        column_mapping = column_mapping
    )
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    profile.to_file(f"{path}/pii_{dag.params.get('data_file')}.html")

def email_reports():
    email = SMTPEmail()
    email.add_attachments(directory_path=f"{get_reports_home()}/{dag.params.get('data_file')}", file_format='.html')
    email.send_email()        
        
start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id="end", dag=dag)
eda_stream = PythonOperator(task_id="ExploratoryDataProfiling", python_callable=generate_eda_profile, dag=dag)
sensitive_data_profile = PythonOperator(task_id="SensitiveDataDiscovery", python_callable=generate_sensitive_data_profile, dag=dag)
if SMTPEmail.availability():
    send_email = PythonOperator(task_id="EmailReports", python_callable=email_reports, dag=dag)
    start >> [eda_stream, sensitive_data_profile]>> send_email >> end
else:
    start >> [eda_stream, sensitive_data_profile]>> end


"""