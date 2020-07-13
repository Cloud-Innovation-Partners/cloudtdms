#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os
import sys
import importlib
from airflow.utils.log.logging_mixin import LoggingMixin


def get_columns(filename):
    columns = None
    with open(f"{os.path.dirname(__file__)}/{filename}", 'r') as f:
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

    meta_data = {
        'code_files': [f for f in os.listdir(os.path.dirname(__file__)) if os.path.isdir(f'{os.path.dirname(__file__)}/{f}') and not f == '__init__.py' and not f =='__pycache__'],
        'data_files': [f[:-4] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.csv') and not f == '__init__.py'],
        'meta-headers': {f[:-4]: get_columns(f) for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.csv') and not f == '__init__.py'},
        'meta-functions': {f: get_functions(f) for f in os.listdir(os.path.dirname(__file__)) if os.path.isdir(f'{os.path.dirname(__file__)}/{f}') and not f == '__init__.py' and not f =='__pycache__'},
        }
    return meta_data
