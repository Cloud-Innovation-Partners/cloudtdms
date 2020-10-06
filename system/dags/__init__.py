#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os
import sys
import importlib
import subprocess
from jinja2 import Template
from airflow import DAG
from airflow import settings
from airflow.models.dag import DagModel
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.configuration import get_airflow_home
from airflow.exceptions import AirflowException

def get_cloudtdms_home():
    """
    Returns `cloudtdms` HOME directory path
    :return: str
    """
    return os.path.dirname(get_airflow_home())


def get_scripts_home():
    """
    Returns `scripts` directory path
    :return: str
    """
    return f"{get_cloudtdms_home()}/config"


def get_providers_home():
    """
    Returns `providers` directory path
    :return:
    """
    return f"{get_airflow_home()}/cloudtdms/providers"


def get_output_data_home():
    """
    Returns `data` directory path
    :return:
    """
    path = f"{get_cloudtdms_home()}/data"
    if not os.path.exists(path):
        os.mkdir(path)

    return path


def get_profiling_data_home():
    """
    Returns `profiling_data` directory path
    :return: str
    """
    path = f"{get_cloudtdms_home()}/profiling_data"
    if not os.path.exists(path):
        os.mkdir(path)

    return path


def get_user_data_home():
    """
    Returns `user-data` directory path
    :return: str
    """
    return f"{get_cloudtdms_home()}/user-data"


def get_config_default_path():
    """
    Returns `config_default.yaml` file path
    :return: str
    """
    return f"{get_cloudtdms_home()}/config_default.yaml"


def get_reports_home():

    return f"{get_cloudtdms_home()}/profiling_reports"


def delete_dag(dag_id):
    p = subprocess.Popen([f"airflow delete_dag -y {dag_id}"],executable="/bin/bash",
                         universal_newlines=True, shell=True)
    (o, e) = p.communicate()


sys.path.append(get_cloudtdms_home())

from system.cloudtdms.utils.template import TEMPLATE, DISCOVER
from system.cloudtdms.providers import get_active_meta_data
from system.cloudtdms.utils import validation

scripts = [f[:-3] for f in os.listdir(get_scripts_home()) if os.path.isfile(f"{get_scripts_home()}/{f}")
           and f.endswith('.py') and not f.startswith('__')]
modules = []

for s in scripts:
    try:
        modules.append((importlib.import_module(f'config.{s}'), s))

    except SyntaxError as se:
        LoggingMixin().log.error(f"SyntaxError: You configuration {se.filename} does not have valid syntax!", exc_info=True)

    except ImportError:
        LoggingMixin().log.error("ImportError: Invalid configuration found, unable to import", exc_info=True)

    except Exception:
        LoggingMixin().log.error("Unknown Exception Occurred!", exc_info=True)

# Create a dag for each `configuration` in config directory
#print(modules)
#print(len(modules))
#print('-'*20)
for (module, name) in modules:

    if hasattr(module, 'STREAM') and isinstance(getattr(module, 'STREAM'), dict):
        stream = getattr(module, 'STREAM')
        meta_data = get_active_meta_data()
        stream['format'] = 'csv'

        # check 'source' attribute is present
        source = f'{get_user_data_home()}/{stream["source"]}.csv' if 'source' in stream else None

        if not validation.check_mandatory_field(stream, name): # means false
            continue

        if not validation.check_schema_type(stream, name):
            continue

        # if not validation.check_source(stream, name):
        #     continue

        if not validation.check_delete(stream,name):
            continue

        # columns in data-file
        all_columns = []
        if source is not None:
            try:
                with open(source, 'r') as f:
                    columns = f.readline()
                    columns = columns.replace('\n', '')
                all_columns = str(columns).split(',')
            except FileNotFoundError:
                LoggingMixin().log.error(f'ValueError: File {source} not found')
                continue
        # get columns to delete
        delete = stream['delete'] if 'delete' in stream else []

        all_columns=[f for f in all_columns if f not in delete]

        # check 'schema' attribute is present
        schema = stream['schema'] if 'schema' in stream else []

        # check 'substitute' attribute is present along with 'source'
        if 'substitute' in stream and source is not None:
            if not validation.check_substitute(stream,name):
                continue
            substitutions = []
            for k, v in stream['substitute'].items():
                v['field_name'] = k
                substitutions.append(v)

            schema += substitutions

        # check 'encrypt' attribute is present along with 'source'

        if 'encrypt' in stream and source is not None:
            if not validation.check_encrypt(stream, name):
                continue
            encryption = [{"field_name": v, "type": "advanced.custom_file", "name": stream['source'], "column": v,
                           "ignore_headers": "no", "encrypt": {"type": stream['encrypt']["type"], "key": stream['encrypt']["encryption_key"]}}
                          for v in stream['encrypt']['columns'] if v in all_columns]
            schema += encryption
            #print('SCHEMA IN ENCRP')
            #print(schema)

        # check 'mask_out' attribute is present along with 'source'

        if 'mask_out' in stream and source is not None:
            mask_outs = [{"field_name": k, "type": "advanced.custom_file", "name": stream['source'],
                          "column": k, "ignore_headers": "no", "mask_out": {"with": v['with'], "characters": v['characters'], "from": v["from"]}}
                         for k, v in stream['mask_out'].items() if k in all_columns]
            schema += mask_outs
        #print('SCHEMA IN MASKOUT')
        #print(schema)
        # check 'shuffle' attribute is present along with 'source'

        if 'shuffle' in stream and source is not None:
            if not validation.check_shuffle(stream, name):
                continue
            shuffle = [{"field_name": v, "type": "advanced.custom_file", "name": stream['source'], "column": v,
                        "ignore_headers": "no", "shuffle": True} for v in stream['shuffle'] if v in all_columns]
            schema += shuffle

        #print('SCHEMA IN SHFFLE')
        #print(schema)

        # check 'nullying' attribute is present along with 'source'

        if 'nullying' in stream and source is not None:
            if not validation.check_nullying(stream,name):
                continue
            nullify = [{"field_name": v, "type": "advanced.custom_file", "name": stream['source'], "column": v,
                        "ignore_headers": "no", "set_null": True} for v in stream['nullying'] if v in all_columns]
            schema += nullify
        #print('SCHEMA AT 209')
        #print(schema)
        if source is not None:
            schema_fields = [f['field_name'] for f in schema]
            remaining_fields = list(set(all_columns) - set(schema_fields))
            remaining = [{"field_name": v, "type": "advanced.custom_file", "name": stream['source'], "column": v,
                            "ignore_headers": "no"} for v in remaining_fields if v in all_columns]
            schema += remaining
        
        stream['schema'] = schema
        #print('SCHEMA AFTER 210')
        #print(schema)
        
        if not schema:
            LoggingMixin().log.error(f"AttributeError: attribute `schema` not found or is empty in {name}.py")
            continue

        #removes duplication
        new_schema = {}
        for s in schema:
            new_schema[s['field_name']] = s
        schema=list(new_schema.values())
        # print(schema)

        attributes = {}
        for col in [f['field_name'] for f in schema]:
            if col not in all_columns:
                all_columns.append(col)
        # ##print(all_columns)

        stream['original_order_of_columns'] = all_columns
        # print(schema)
        schema.sort(reverse=True, key=lambda x: x['type'].split('.')[1])
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

        template = Template(TEMPLATE)
        output = template.render(
            data={
                'dag_id': str(name),
                'frequency': stream['frequency'],
                'stream' : stream,
                'attributes' : attributes
            }
        )
        dag_file_path = f"{get_airflow_home()}/dags/config_{name}.py"
        with open(dag_file_path, 'w') as f:
            f.write(output)

        LoggingMixin().log.info(f"Creating DAG: {name}")
    else:
        LoggingMixin().log.error(f"No `STREAM` attribute found in configuration {name}.py")

# list files in user-data

profiling_data_files = [f[:-4] for f in os.listdir(get_profiling_data_home()) if f.endswith('.csv') and not f == '__init__.py']

# create dag for profiling user data

for file in profiling_data_files:
    template = Template(DISCOVER)
    output = template.render(
        data={
            'dag_id': str(f"profile_{file}").replace('-', '_').replace(' ', '_').replace(':','_'),
            'frequency': 'once',
            'data_file': file
        }
    )
    dag_file_path = f"{get_airflow_home()}/dags/profile_{file}.py"
    with open(dag_file_path, 'w') as f:
        f.write(output)

    LoggingMixin().log.info(f"Creating DAG: profile_{file}.py")

# fetch all dags in directory

dags = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.py') and not f == '__init__.py']

# fetch list of loaded dags from meta-db

loaded_dags = settings.Session.query(DagModel.dag_id, DagModel.fileloc).all()

# delete dags from meta-db

for l_dag in loaded_dags:
    (dag_id, fileloc) = l_dag
    filename = os.path.basename(fileloc)[:-3]
    if filename not in [f"config_{f}" for f in scripts] + [f"profile_{f}" for f in profiling_data_files]:
        try:
            if os.path.exists(fileloc):
                os.remove(fileloc)
            else:
                LoggingMixin().log.warning("{} file doesn't exists !".format(filename))

            delete_dag(dag_id)

        except Exception as e:
            LoggingMixin().log.error(str(e))
