#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os
import importlib
import pathlib
from itertools import chain
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.configuration import get_airflow_home


def get_columns(path):
    columns = None
    with open(path, 'r') as f:
        columns = f.readline().replace('\n', '')
    return columns.split(',')


def get_functions(module):
    try:
        mod = importlib.import_module(f'system.cloudtdms.providers.{module}')
        return [f for f in dir(mod) if not f.startswith('__')]
    except ImportError:
        LoggingMixin().log.info(f"ImportError: Unable to import `{module}` code-file!")
        raise


def get_active_meta_data():

    data_files = chain([(os.path.basename(f)[:-4], f) for f in list(pathlib.Path(os.path.dirname(__file__)).rglob('*.csv'))],
                       [(f[:-4], f"{os.path.dirname(get_airflow_home())}/user-data/{f}") for f in
                        os.listdir(f"{os.path.dirname(get_airflow_home())}/user-data") if f.endswith('.csv')])

    meta_data = {
        'code_files': [f for f in os.listdir(os.path.dirname(__file__)) if os.path.isdir(f'{os.path.dirname(__file__)}/{f}') and not f == '__init__.py' and not f =='__pycache__'],
        'data_files': [os.path.basename(f)[:-4] for f in list(pathlib.Path(os.path.dirname(__file__)).rglob('*.csv'))] + [f[:-4] for f in os.listdir(f"{os.path.dirname(get_airflow_home())}/user-data") if f.endswith('.csv')],
        'meta-headers': {data_file_name: get_columns(path) for (data_file_name, path) in data_files},
        'meta-functions': {f: get_functions(f) for f in os.listdir(os.path.dirname(__file__)) if os.path.isdir(f'{os.path.dirname(__file__)}/{f}') and not f == '__init__.py' and not f =='__pycache__'},
        }
    return meta_data
