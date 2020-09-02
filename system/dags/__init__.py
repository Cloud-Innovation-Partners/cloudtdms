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
    return f"{get_cloudtdms_home()}/scripts"


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



def delete_dag(dag_id):
    p = subprocess.Popen([f"airflow delete_dag -y {dag_id}"],executable="/bin/bash",
                         universal_newlines=True, shell=True)
    (o, e) = p.communicate()


sys.path.append(get_cloudtdms_home())

from system.cloudtdms.utils.template import TEMPLATE
from system.cloudtdms.providers import get_active_meta_data
from system.cloudtdms.utils import validation


scripts = [f[:-3] for f in os.listdir(get_scripts_home()) if os.path.isfile(f"{get_scripts_home()}/{f}")
           and f.endswith('.py') and not f.startswith('__')]
modules = []

for s in scripts:
    try:
        modules.append((importlib.import_module(f'scripts.{s}'), s))

    except SyntaxError as se:
        LoggingMixin().log.error(f"SyntaxError: You script {se.filename} does not have valid syntax!", exc_info=True)

    except ImportError:
        LoggingMixin().log.error("ImportError: Invalid script found, unable to import", exc_info=True)

    except Exception:
        LoggingMixin().log.error("Unknown Exception Occurred!", exc_info=True)

# Create a dag for each `script` in scripts directory

for (module, name) in modules:

    stream = getattr(module, 'STREAM')

    if hasattr(module, 'STREAM') and isinstance(getattr(module, 'STREAM'), dict):
        meta_data = get_active_meta_data()
        stream['format'] = 'csv'

        # check 'source' attribute is present
        source = f'{get_cloudtdms_home()}/user-data/{stream["source"]}.csv' if 'source' in stream else None

        if not validation.check_mandotry_field(stream, name): # means false
            continue

        if not validation.check_schema_type(stream, name):
            continue

        if not validation.check_source(stream, name):
            continue

        if not validation.check_delete(stream,name):
            continue

        # columns in data-file
        all_columns = []
        if source is not None:
            with open(source, 'r') as f:
                columns = f.readline()
                columns = columns.replace('\n', '')
            all_columns = str(columns).split(',')

        # get columns to delete
        delete = stream['delete'] if 'delete' in stream else []

        all_columns = list(set(all_columns) - set(delete))

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

        # check 'mask_out' attribute is present along with 'source'

        if 'mask_out' in stream and source is not None:
            mask_outs = [{"field_name": k, "type": "advanced.custom_file", "name": stream['source'],
                          "column": k, "ignore_headers": "no", "mask_out": {"with": v['with'], "characters": v['characters'], "from": v["from"]}}
                         for k, v in stream['mask_out'].items() if k in all_columns]
            schema += mask_outs

        # check 'shuffle' attribute is present along with 'source'

        if 'shuffle' in stream and source is not None:
            if not validation.check_shuffle(stream, name):
                continue
            shuffle = [{"field_name": v, "type": "advanced.custom_file", "name": stream['source'], "column": v,
                        "ignore_headers": "no", "shuffle": True} for v in stream['shuffle'] if v in all_columns]
            schema += shuffle

        # check 'nullying' attribute is present along with 'source'

        if 'nullying' in stream and source is not None:
            if not validation.check_nullying(stream,name):
                continue
            nullify = [{"field_name": v, "type": "advanced.custom_file", "name": stream['source'], "column": v,
                        "ignore_headers": "no", "set_null": True} for v in stream['nullying'] if v in all_columns]
            schema += nullify

        if source is not None:
            schema_fields = [f['field_name'] for f in schema]
            remaining_fields = list(set(all_columns) - set(schema_fields))
            remaining = [{"field_name": v, "type": "advanced.custom_file", "name": stream['source'], "column": v,
                            "ignore_headers": "no"} for v in remaining_fields if v in all_columns]
            schema += remaining

        attributes = {}
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
        dag_file_path = f"{get_airflow_home()}/dags/{name}.py"
        with open(dag_file_path, 'w') as f:
            f.write(output)

        LoggingMixin().log.info(f"Creating DAG: {name}")
    else:
        LoggingMixin().log.warn(f"No `STREAM` attribute found in script {name}.py")

# fetch all dags in directory

dags = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.py') and not f == '__init__.py']

# fetch list of loaded dags from meta-db

loaded_dags = settings.Session.query(DagModel.dag_id, DagModel.fileloc).all()

# delete dags from meta-db

for l_dag in loaded_dags:
    (dag_id, fileloc) = l_dag
    filename = os.path.basename(fileloc)[:-3]
    if filename not in scripts:
        try:
            if os.path.exists(fileloc):
                os.remove(fileloc)
            else:
                LoggingMixin().log.warning("{} file doesn't exists !".format(filename))

            delete_dag(dag_id)

        except Exception as e:
            LoggingMixin().log.error(str(e))
