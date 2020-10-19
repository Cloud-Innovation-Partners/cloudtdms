#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os
import sys
import importlib
import subprocess
from jinja2 import Template
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


def create_profiling_dag(file_name, owner):
    file_name = file_name[:-4]
    dag_template = Template(DISCOVER)
    dag_output = dag_template.render(
        data={
            'dag_id': str(f"profile_{file_name}").replace('-', '_').replace(' ', '_').replace(':', '_'),
            'frequency': 'once',
            'data_file': file_name,
            'owner': owner.replace('-', '_').replace(' ', '_').replace(':', '_').replace(' ', '')
        }
    )
    dag_file = f"{get_airflow_home()}/dags/profile_{file_name}.py"
    with open(dag_file, 'w') as g:
        g.write(dag_output)

    LoggingMixin().log.info(f"Creating DAG: profile_{file_name}.py")


scripts = []
modules = []

for config in os.walk(f"{get_scripts_home()}"):
    try:
        root, dirs, files = config
        if len(dirs) != 0:
            for each_dir in dirs:
                if '__init__.py' not in os.listdir(f"{root}/{each_dir}"):
                    open(f"{root}/{each_dir}/__init__.py", 'w').close()
        files = list(filter(lambda x: x.endswith('.py') and x != '__init__.py', files))
        scripts += files
        root = root.replace(f"{get_cloudtdms_home()}/", '').replace('/', '.')
        packages = list(map(lambda x: f"{root}.{x}"[:-3], files))
        root = os.path.basename(root.replace('.', '/')) if os.path.basename(root.replace('.', '/')) != 'config' else 'CloudTDMS'
        modules += list(map(lambda x: (importlib.import_module(f'{x}'), x.rsplit('.', 1)[1], root), packages))

    except SyntaxError as se:
        LoggingMixin().log.error(f"SyntaxError: You configuration {se.filename} does not have valid syntax!", exc_info=True)

    except ImportError:
        LoggingMixin().log.error("ImportError: Invalid configuration found, unable to import", exc_info=True)

    except Exception:
        LoggingMixin().log.error("Unknown Exception Occurred!", exc_info=True)

# Create a dag for each `configuration` in config directory

for (module, name, app) in modules:

    if hasattr(module, 'STREAM') and isinstance(getattr(module, 'STREAM'), dict):
        stream = getattr(module, 'STREAM')
        meta_data = get_active_meta_data()
        stream['format'] = 'csv'

        # check 'source' attribute is present
        source = stream['source'] if 'source' in stream else None

        if source is None:
            # if type(source) is str and not os.path.exists(f'{get_user_data_home()}/{str(source).replace(".csv", "")}.csv'):
            #     LoggingMixin().log.error(f"FileNotFound: No file available in user-data folder with name {str(source).replace('.csv', '')}.csv")
            #     continue

            if not validation.check_mandatory_field(stream, name):      # means false
                continue

            if not validation.check_schema_type(stream, name):
                continue

            # check 'schema' attribute is present
            schema = stream['schema'] if 'schema' in stream else []

            if not schema:
                LoggingMixin().log.error(f"AttributeError: attribute `schema` not found or is empty in {name}.py")
                continue

            stream['original_order_of_columns'] = [f['field_name'] for f in schema]

            schema.sort(reverse=True, key=lambda x: x['type'].split('.')[1])

            attributes = {}
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
                    'dag_id': f"data_{app}_{name}",
                    'frequency': stream['frequency'],
                    'owner': app.replace('-', '_').replace(' ', '_').replace(':', '_').replace(' ',''),
                    'stream': stream,
                    'attributes': attributes,
                    'source': source if source is not None else {},
                    'destination': stream['destination'] if 'destination' in stream.keys() else {}
                }
            )
            dag_file_path = f"{get_airflow_home()}/dags/data_{name}.py"
            with open(dag_file_path, 'w') as f:
                f.write(output)

            LoggingMixin().log.info(f"Creating DAG: {name}")
        else:
            if not validation.check_mandatory_field(stream, name):      # means false
                continue
            template = Template(TEMPLATE)
            output = template.render(
                data={
                    'dag_id': f"data_{app}_{name}",
                    'frequency': stream['frequency'],
                    'owner': app.replace('-', '_').replace(' ', '_').replace(':', '_').replace(' ', ''),
                    'stream': stream,
                    'attributes': {},
                    'source': source if source is not None else [],
                    'destination': stream['destination'] if 'destination' in stream.keys() else {}
                }
            )
            dag_file_path = f"{get_airflow_home()}/dags/data_{name}.py"
            with open(dag_file_path, 'w') as f:
                f.write(output)

            LoggingMixin().log.info(f"Creating DAG: {name}")

    else:
        LoggingMixin().log.error(f"No `STREAM` attribute found in configuration {name}.py")

# list files in user-data

profiling_data_files = []

# create dag for profiling user data

for profile in os.walk(get_profiling_data_home()):
    root, dirs, files = profile
    files = list(filter(lambda x: x.endswith('.csv'), files))
    root = root.replace(f"{get_cloudtdms_home()}/", '')
    root = os.path.basename(root) if os.path.basename(root) != 'profiling_data' else 'CloudTDMS'
    list(map(create_profiling_dag, files, [f'{root}']*len(files)))
    profiling_data_files += files

# fetch all dags in directory

dags = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.py') and not f == '__init__.py']

# fetch list of loaded dags from meta-db

loaded_dags = settings.Session.query(DagModel.dag_id, DagModel.fileloc).all()

# delete dags from meta-db

for l_dag in loaded_dags:
    (dag_id, fileloc) = l_dag
    filename = os.path.basename(fileloc)[:-3]
    if filename not in [f"data_{f}"[:-3] for f in scripts] + [f"profile_{f}"[:-4] for f in profiling_data_files]:
        try:
            if os.path.exists(fileloc):
                os.remove(fileloc)
            else:
                LoggingMixin().log.warning("{} file doesn't exists !".format(filename))

            delete_dag(dag_id)

        except Exception as e:
            LoggingMixin().log.error(str(e))
