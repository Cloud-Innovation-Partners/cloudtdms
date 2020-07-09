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


def delete_dag(dag_id):
    p = subprocess.Popen([f"airflow delete_dag -y {dag_id}"],executable="/bin/bash",
                         universal_newlines=True, shell=True)
    (o, e) = p.communicate()


sys.path.append(get_cloudtdms_home())

from system.cloudtdms.utils.template import TEMPLATE

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
        template = Template(TEMPLATE)
        output = template.render(
            data={
                'dag_id': str(name),
                'frequency': stream['frequency'],
                'stream' : stream
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
