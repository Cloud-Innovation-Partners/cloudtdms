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
