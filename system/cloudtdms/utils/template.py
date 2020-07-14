#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

TEMPLATE = """
import sys
import os
import importlib
import random
import pandas as pd
from datetime import datetime, timedelta
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
            result = fcn(number)
        else:
            result = fcn(number,arg)
        data_frame[name] = pd.Series(result)

def args_dict(scheme, default_keys):
    args={}
    for key, value in scheme.items():
        if key =='type':
            func_name=scheme['type'].split('.')[1]
        if key not in default_keys:
            args[key]=value
    return func_name,args
            
def get_method_args(schema):
    args_array={}
    default_keys=['field_name','type']
    for scheme in schema:
        keys = list(scheme.keys())
        nkeys=len(list(scheme.keys()))
        
        if nkeys >2 and keys not in default_keys:
            (func_name,args)=args_dict(scheme, default_keys)
            args_array[func_name]=args
    
    return args_array
        
        


def data_generator():
    meta_data = providers.get_active_meta_data()
    stream = dag.params.get('stream')
    schema = stream['schema']
    attributes = dag.params.get('attributes')
    nrows = stream['number']
    ncols = sum([len(f) for f in attributes.values()])
    columns = []
    labels = [columns.extend(f) for f in attributes.values()]
    data_frame = pd.DataFrame(pd.np.zeros((nrows, ncols))*pd.np.nan, columns=columns)    
    
    for attrib in attributes:
        if attrib in meta_data['data_files']:
            df = pd.read_csv(f"{get_providers_home()}/{attrib}.csv", usecols=attributes[attrib])
            df_temp = pd.DataFrame(index=range(nrows), columns=attributes[attrib])
            for i in range(nrows):
                df_temp.iloc[i] = df.iloc[random.randrange(len(df))]
                            
            data_frame[attributes[attrib]] = df_temp[attributes[attrib]]
        elif attrib in meta_data['code_files']:
            mod = importlib.import_module(f"system.cloudtdms.providers.{attrib}")
            methods = [(getattr(mod, m), m) for m in attributes[attrib]]
            args_array=get_method_args(schema)
            print(args_array)
            generate_iterator(data_frame, methods,args_array)     
    
    
    for scheme in schema:
        field_name = scheme['field_name']
        column_name = scheme['type'].split('.')[1]
        data_frame.rename(columns={column_name:field_name}, inplace=True)

    data_frame.to_csv(f"{get_output_data_home()}/{stream['title']}.csv", index=False)
    
start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id="end", dag=dag)
stream = PythonOperator(task_id="GenerateStream", python_callable=data_generator, dag=dag)

start >> stream >> end

"""