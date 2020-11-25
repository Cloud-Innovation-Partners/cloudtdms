#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os
import datetime
import sys
import importlib
import subprocess
import jinja2
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


def get_templates_home():
    return f"{get_airflow_home()}/cloudtdms/templates"


def delete_dag(dag_id):
    p = subprocess.Popen([f"airflow delete_dag -y {dag_id}"], executable="/bin/bash",
                         universal_newlines=True, shell=True)
    (o, e) = p.communicate()


sys.path.append(get_cloudtdms_home())

from system.cloudtdms.providers import get_active_meta_data
from system.cloudtdms.utils.validation import Validation


def filter_profiling(profiling_file_path, dag_file_path, dag_delete=False, owner=None):
    profiling_stat = os.stat(profiling_file_path)
    profiling_mtime = profiling_stat.st_mtime
    profiling_timestamp = datetime.datetime.fromtimestamp(profiling_mtime).strftime('%Y-%m-%d-%H:%M:%S')
    try:
        dag_stat = os.stat(dag_file_path)
        dag_mtime = dag_stat.st_mtime
        dag_timestamp = datetime.datetime.fromtimestamp(dag_mtime).strftime('%Y-%m-%d-%H:%M:%S')
    except FileNotFoundError:
        LoggingMixin().log.info(f" Creating DAG {os.path.basename(dag_file_path)} for the first time ")
        return True
    # print(f"PROFILING_{os.path.basename(profiling_file_path).split('.')[0]}:{profiling_timestamp}")
    # print(f"DAG_{os.path.basename(dag_file_path).split('.')[0]}:{dag_timestamp}")
    result = profiling_timestamp > dag_timestamp
    if result:
        LoggingMixin().log.info(f"{os.path.basename(profiling_file_path)} is modified. Creating new profiling report...")
        if dag_delete and os.path.exists(dag_file_path):
            dag_id = f"profile_{os.path.basename(profiling_file_path).split('.')[0]}"
            os.remove(dag_file_path)
            delete_dag(dag_id)
            print(f"DELETING DAG_ID: {dag_id}")
    return result


def create_profiling_dag(file_name, owner):
    file_name, extension = os.path.splitext(file_name)
    TEMPLATE_FILE = "profiling_data_dag.py.j2"
    template = templateEnv.get_template(TEMPLATE_FILE)
    dag_output = template.render(
        data={
            'dag_id': str(f"profile_{file_name}").replace('-', '_').replace(' ', '_').replace(':', '_'),
            'frequency': 'once',
            'data_file': f"{file_name}{extension}",
            'owner': owner.replace('-', '_').replace(' ', '_').replace(':', '_').replace(' ', '')
        }
    )
    dag_file = f"{get_airflow_home()}/dags/profile_{file_name}.py"
    profile_file= f"{get_profiling_data_home()}/{file_name}{extension}"
    # print(f"DAG FILE PATH: {dag_file}")
    # print(f"PROFILE FILE PATH: {profile_file}")

    if filter_profiling(profiling_file_path=profile_file, dag_file_path= dag_file, dag_delete= True, owner=owner):
        with open(dag_file, 'w') as g:
            g.write(dag_output)
        LoggingMixin().log.info(f"Creating DAG: profile_{file_name}.py")

def filter_updated_dag(config_file_path, dag_file_path, dag_delete=False, owner=None):

    config_stat = os.stat(config_file_path)
    config_mtime = config_stat.st_mtime
    config_timestamp = datetime.datetime.fromtimestamp(config_mtime).strftime('%Y-%m-%d-%H:%M:%S')
    # config_mtime=os.path.getmtime(config_file_path)

    try:
        dag_stat = os.stat(dag_file_path)
        dag_mtime = dag_stat.st_mtime
        dag_timestamp = datetime.datetime.fromtimestamp(dag_mtime).strftime('%Y-%m-%d-%H:%M:%S')
    except FileNotFoundError:
        LoggingMixin().log.info(f" Creating DAG {os.path.basename(dag_file_path)} for the first time ")
        return True

    # print(f"CONFIG_{os.path.basename(config_file_path).split('.')[0]}: {config_timestamp}")
    # print(f"DAG_{os.path.basename(dag_file_path).split('.')[0]}: {dag_timestamp}")

    result = config_timestamp > dag_timestamp

    if result:
        LoggingMixin().log.info(
            f"config file {os.path.basename(config_file_path)} is modified. Creating updated DAG...")
        if dag_delete and os.path.exists(dag_file_path):
            dag_id = f"data_{owner}_{os.path.basename(config_file_path).split('.')[0]}"
            os.remove(dag_file_path)
            delete_dag(dag_id)
            print(f"DELETING DAG_ID: {dag_id}")
    return result


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

        owner = os.path.basename(root) if os.path.basename(root) != 'config' else 'CloudTDMS'
        modified_dags = list(
            filter(lambda x:
                   filter_updated_dag(config_file_path=f"{root}/{x}",
                                      dag_file_path=f"{get_airflow_home()}/dags/data_{x}",
                                      dag_delete=True,
                                      owner=owner),
                   files
                   )
        )

        files = modified_dags

        root = root.replace(f"{get_cloudtdms_home()}/", '').replace('/', '.')
        packages = list(map(lambda x: f"{root}.{x}"[:-3], files))
        root = os.path.basename(root.replace('.', '/')) if os.path.basename(
            root.replace('.', '/')) != 'config' else 'CloudTDMS'
        modules += list(map(lambda x: (importlib.import_module(f'{x}'), x.rsplit('.', 1)[1], root), packages))

    except SyntaxError as se:
        LoggingMixin().log.error(f"SyntaxError: You configuration {se.filename} does not have valid syntax!",
                                 exc_info=True)

    except ImportError:
        LoggingMixin().log.error("ImportError: Invalid configuration found, unable to import", exc_info=True)

    except Exception:
        LoggingMixin().log.error("Unknown Exception Occurred!", exc_info=True)

# Load templates environment

templateLoader = jinja2.FileSystemLoader(searchpath=get_templates_home())
templateEnv = jinja2.Environment(loader=templateLoader)

# Create a dag for each `configuration` in config directory

for (module, name, app) in modules:

    if hasattr(module, 'STREAM') and isinstance(getattr(module, 'STREAM'), dict):
        stream = getattr(module, 'STREAM')

        # Validate Syntax

        if not Validation.validate(stream, name):
            continue

        meta_data = get_active_meta_data()

        # set format to csv
        stream['format'] = 'csv'

        # check 'source' attribute is present
        source = stream['source'] if 'source' in stream else None

        if source is None:
            # check 'schema' attribute is present
            schema = stream['synthetic'] if 'synthetic' in stream else []

            if not schema:
                LoggingMixin().log.error(f"AttributeError: attribute `synthetic` not found or is empty in {name}.py")
                continue

            stream['original_order_of_columns'] = [f['field_name'] for f in schema]

            try:
                schema.sort(reverse=True, key=lambda x: x['type'].split('.')[1])
            except IndexError:
                LoggingMixin().log.warn(f"`type` field not specified for {name}.py")
                continue

            attributes = {}
            for scheme in schema:
                provider, generator = scheme['type'].split('.')

                if provider in meta_data['code_files']:
                    if generator in meta_data['meta-functions'][provider]:
                        if provider not in attributes:
                            attributes[provider] = [generator]
                        else:
                            attributes[provider].append(generator)
                    else:
                        raise AirflowException(f"TypeError: no data available for type {generator} ")
                else:
                    raise AirflowException(f"IOError: no provider  found for {provider} ")

            stream['schema'] = schema

            TEMPLATE_FILE = "synthetic_data_dag.py.j2"
            template = templateEnv.get_template(TEMPLATE_FILE)
            output = template.render(
                data={
                    'dag_id': f"data_{app}_{name}",
                    'frequency': stream['frequency'],
                    'owner': app.replace('-', '_').replace(' ', '_').replace(':', '_').replace(' ', ''),
                    'stream': stream,
                    'attributes': attributes if len(attributes) != 0 else None,
                    'source': source if source is not None else {},
                    'destination': stream['destination'] if 'destination' in stream.keys() else {}
                }
            )
            dag_file_path = f"{get_airflow_home()}/dags/data_{name}.py"
            with open(dag_file_path, 'w') as f:
                f.write(output)

            LoggingMixin().log.info(f"Creating DAG: {name}")
        else:
            if type(source) is dict:
                TEMPLATE_FILE = "synthetic_data_dag.py.j2"
                template = templateEnv.get_template(TEMPLATE_FILE)
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
                LoggingMixin().log.error(f"AttributeError: `source` attribute must be of type dict in {name}")

    else:
        LoggingMixin().log.error(f"No `STREAM` attribute found in configuration {name}.py")

# list files in user-data

profiling_data_files = []

# create dag for profiling user data

for profile in os.walk(get_profiling_data_home()):
    root, dirs, files = profile
    files = list(filter(lambda x: x.endswith('.csv') or x.endswith('.json'), files))
    root = root.replace(f"{get_cloudtdms_home()}/", '')
    root = os.path.basename(root) if os.path.basename(root) != 'profiling_data' else 'CloudTDMS'
    list(map(create_profiling_dag, files, [f'{root}'] * len(files)))
    profiling_data_files += list(
        map(lambda x: x[:-4] if x.endswith('.csv') else x[:-5] if x.endswith('.json') else x[:-4], files))

# fetch all dags in directory

dags = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.py') and not f == '__init__.py']

# fetch list of loaded dags from meta-db

loaded_dags = settings.Session.query(DagModel.dag_id, DagModel.fileloc).all()

# delete dags from meta-db

for l_dag in loaded_dags:
    (dag_id, fileloc) = l_dag
    filename = os.path.basename(fileloc)[:-3]
    if filename not in [f"data_{f}"[:-3] for f in scripts] + [f"profile_{f}" for f in profiling_data_files]:
        try:
            if os.path.exists(fileloc):
                os.remove(fileloc)
            else:
                LoggingMixin().log.warning("{} file doesn't exists !".format(filename))

            delete_dag(dag_id)

        except Exception as e:
            LoggingMixin().log.error(str(e))
