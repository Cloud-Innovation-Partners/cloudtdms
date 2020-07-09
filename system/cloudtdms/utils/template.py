#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

TEMPLATE = """
import sys
import os
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


def data_generator():
    meta_data = providers.get_active_meta_data()
    stream = dag.params.get('stream')
    attributes = dag.params.get('attributes')
    data_frame = pd.DataFrame()
    for attrib in attributes:
        df = pd.read_csv(f"{get_providers_home()}/{attrib}.csv", usecols=attributes[attrib])
        data_frame[attributes[attrib]] = df[attributes[attrib]]
    
    schema = stream['schema']

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