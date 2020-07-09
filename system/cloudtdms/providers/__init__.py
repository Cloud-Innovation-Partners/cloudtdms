#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os


def get_columns(filename):
    columns = None
    with open(f"{os.path.dirname(__file__)}/{filename}", 'r') as f:
        columns = f.readline().replace('\n', '')
    return columns.split(',')


def get_active_meta_data():

    meta_data = {
        'data_files': [f[:-4] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.csv') and not f == '__init__.py'],
        'meta-headers': {f[:-4]: get_columns(f) for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.csv') and not f == '__init__.py'}
        }

    return meta_data
