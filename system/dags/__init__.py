#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os
import sys
import importlib
import subprocess
import grp
import pwd
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
    if hasattr(module, 'STREAM') and isinstance(getattr(module, 'STREAM'), dict):
        stream = getattr(module, 'STREAM')
        meta_data = get_active_meta_data()
        schema = stream['schema']
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
        os.chmod(dag_file_path, 0o664)
        os.chown(dag_file_path, pwd.getpwnam("cloudtdms").pw_uid, grp.getgrnam("cloudtdms").gr_gid)
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
