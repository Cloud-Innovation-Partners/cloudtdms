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
            'stream': {{ data.stream }}
        }
)


def data_generator():
    meta_data = providers.get_active_meta_data()
    stream = dag.params.get('stream')
    schema = stream['schema']
    data_frame = pd.DataFrame()
    for scheme in schema:
        (data, column) = tuple(scheme['type'].split('.'))
        if data in meta_data['data_files']:
            if column in meta_data['meta-headers'][data]:
                # TODO-DataFrame Logic
                LoggingMixin().log.info("OK...")
            else:
                raise AirflowException(f"TypeError: no data available for type {column} ")
        else:
            raise AirflowException(f"IOError: no data file found {data}.csv ")
    


start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id="end", dag=dag)
stream = PythonOperator(task_id="GenerateStream", python_callable=data_generator, dag=dag)

start >> stream >> end

"""