
import base64
import requests
import os
import json
import ijson
import tempfile
import io
import yaml
from simple_salesforce import Salesforce
import pandas as pd
from datetime import datetime
from airflow.utils.log.logging_mixin import LoggingMixin
from system.dags import get_output_data_home, get_config_default_path, get_user_data_home
from system.cloudtdms.extras import DESTINATION_UPLOAD_LIMIT, SOURCE_DOWNLOAD_LIMIT


class CTDMS2SalesForce:

    def __init__(self, instance, username, password, security_token, table_name, prefix, execution_date, format=None, connection=None):
        self.sales_force_instance = instance
        self.sales_force_username = username
        self.sales_force_password = password
        self.sales_force_security_token = security_token
        self.name = str(table_name).upper()
        self.table_name = table_name
        self.file_prefix = prefix
        self.data = None
        self.execution_date = execution_date
        self.format = format
        self.connection_name = connection
        self.file_name = f"{os.path.basename(prefix)}_{str(execution_date)[:19].replace('-','_').replace(':','_')}.csv" if format is None else f"{os.path.basename(prefix)}_{str(execution_date)[:19].replace('-','_').replace(':','_')}.{format}"

    def generate_access_token(self, username, password, id, secret):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }
        response = requests.request("POST",
                                    url="https://{}.salesforce.com/services/oauth2/token".format(self.sales_force_instance),
                                    params={
                                        "grant_type": "password",
                                        "client_id": id,
                                        "client_secret": secret,
                                        "username": username,
                                        "password": password
                                    },
                                    headers=headers
                                    )
        # Throw an error for Bad Status Code
        response.raise_for_status()
        return json.loads(response.text).get('access_token')

    def generate_job_id(self, access_token):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'X-SFDC-Session': access_token
        }
        response = requests.request("POST",
                                    url="https://{}.salesforce.com/services/async/50.0/job".format(
                                        self.sales_force_instance),
                                    headers=headers,
                                    data=json.dumps(
                                        {
                                            "operation": "insert",
                                            "object": self.table_name,
                                            "contentType": "JSON"
                                        })
                                    )
        # Throw an error for Bad Status Code
        response.raise_for_status()
        return json.loads(response.text).get('id')

    def describe_object(self, access_token):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }
        response = requests.request("GET",
                                    url="https://{}.salesforce.com/services/data/v50.0/sobjects/{}/describe/".format(
                                        self.sales_force_instance, self.table_name),
                                    headers=headers
                                    )
        # Throw an error for Bad Status Code
        response.raise_for_status()

        objects = ijson.items(io.StringIO(response.text), 'fields.item')
        fields = [f.get('name') for f in objects]
        return ','.join(fields)

    def upload(self):
        """
        This is a convenience function used to upload the data
        :return:
        """
        synthetic_data_path = f"{get_output_data_home()}/{self.file_prefix}/{self.file_name}"
        if os.path.exists(synthetic_data_path):
            if self.format == 'json':
                df = pd.read_json(f"{synthetic_data_path}", nrows=DESTINATION_UPLOAD_LIMIT, lines=True, orient='records')
            else:
                df = pd.read_csv(f"{synthetic_data_path}", nrows=DESTINATION_UPLOAD_LIMIT)
            a = df.to_json(lines=True, orient='records')
            objects = (json.loads(f) for f in io.StringIO(a).readlines())
            self.data = list(objects)

            username = base64.b64decode(str(self.sales_force_username).encode()).decode('utf-8')
            password = base64.b64decode(str(self.sales_force_password).encode()).decode('utf-8')
            security_token = base64.b64decode(str(self.sales_force_security_token).encode()).decode('utf-8')

            sf = Salesforce(
                instance=self.sales_force_instance,
                username=username,
                password=password,
                security_token=security_token
            )

            response = sf.bulk.__getattr__(self.table_name).insert(self.data)
            total = len(response)
            success = 0
            for r in response:
                if not r.get('success'):
                    LoggingMixin().log.error(r.get('errors'))
                else:
                    success += 1

            LoggingMixin().log.info(f"Upload Status : {success}/{total}")
        else:
            LoggingMixin().log.error(f"No Synthetic Data Found @ {synthetic_data_path}!")
            raise FileNotFoundError

    def download(self, limit=SOURCE_DOWNLOAD_LIMIT):
        """
        This is a convenience function used to download the data
        :return:
        """
        username = base64.b64decode(str(self.sales_force_username).encode()).decode('utf-8')
        password = base64.b64decode(str(self.sales_force_password).encode()).decode('utf-8')
        security_token = base64.b64decode(str(self.sales_force_security_token).encode()).decode('utf-8')

        sf = Salesforce(
            instance=self.sales_force_instance,
            username=username,
            password=password,
            security_token=security_token
        )

        columns = [f.get('name') for f in sf.__getattr__(self.table_name).describe().get('fields')]

        query = f"SELECT {', '.join(columns)} FROM {self.table_name} LIMIT {SOURCE_DOWNLOAD_LIMIT}"

        fetch_results = sf.query(query).get('records')

        df = pd.DataFrame(fetch_results)

        df.columns = [f"salesforce.{self.connection_name}.{self.table_name}.{f}" for f in df.columns]

        file_name = f"salesforce_{self.connection_name}_{os.path.dirname(self.file_prefix)}_{os.path.basename(self.file_prefix)}_{str(self.execution_date)[:19].replace('-','_').replace(':','_')}.csv"

        try:
            df.to_csv(f'{get_user_data_home()}/.__temp__/{file_name}', index=False)
        except FileNotFoundError:
            os.makedirs(f'{get_user_data_home()}/.__temp__/')
            df.to_csv(f'{get_user_data_home()}/.__temp__/{file_name}', index=False)

        LoggingMixin().log.info("[{}] API request end time {}".format(self.name, datetime.now()))

    @staticmethod
    def get_sales_force_config_default():
        config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
        if config is not None and config.get('salesforce', None) is not None:
            return config.get('salesforce')
        else:
            raise KeyError('config_default.yaml has no SalesForce entry')


def salesforce_upload(**kwargs):

    execution_date = kwargs.get('execution_date', None)     # dag execution date
    table_name = kwargs.get('table_name')       # SalesForce table name
    prefix = kwargs.get('prefix')       # title of the synthetic data config file
    connection = kwargs.get('connection')
    format = kwargs.get('format')
    # Load SalesForce Instance From config_default.yaml
    sales_force_config = CTDMS2SalesForce.get_sales_force_config_default()

    username, password, instance, security_token = None, None, None, None
    try:
        username = sales_force_config.get(connection).get('username', None)
        password = sales_force_config.get(connection).get('password', None)
        instance = sales_force_config.get(connection).get('host', None)
        security_token = sales_force_config.get(connection).get('security_token', None)


    except AttributeError:
        LoggingMixin().log.error(f'SalesForce credentials not available for {connection} in config_default.yaml', exc_info=True)
        raise

    if username is not None and password is not None and instance is not None and security_token is not None:
        sales_force = CTDMS2SalesForce(
            instance=instance,
            username=username,
            password=password,
            security_token=security_token,
            table_name=table_name,
            prefix=prefix,
            execution_date=execution_date,
            format=format,
            connection=connection
        )
        sales_force.upload()
    else:
        LoggingMixin().log.error(f'SalesForce credentials not available for {instance} in config_default.yaml')
        raise AttributeError(f'SalesForce credentials not available for {instance} in config_default.yaml')


def salesforce_download(**kwargs):
    execution_date = kwargs.get('execution_date', None)  # dag execution date
    table_name = kwargs.get('table_name')  # SalesForce table name
    prefix = kwargs.get('prefix')  # title of the synthetic data config file
    connection = kwargs.get('connection')
    limit = kwargs.get('limit') if kwargs.get('limit') != "" else 5000
    # Load SalesForce Instance From config_default.yaml
    sales_force_config = CTDMS2SalesForce.get_sales_force_config_default()

    username, password, instance, security_token = None, None, None, None
    try:
        username = sales_force_config.get(connection).get('username', None)
        password = sales_force_config.get(connection).get('password', None)
        instance = sales_force_config.get(connection).get('host', None)
        security_token = sales_force_config.get(connection).get('security_token', None)
    except AttributeError:
        LoggingMixin().log.error(f'SalesForce credentials not available for {connection} in config_default.yaml', exc_info=True)
        raise
    
    if username is not None and password is not None and instance is not None and security_token is not None:
        sales_force = CTDMS2SalesForce(
            instance=instance,
            username=username,
            password=password,
            security_token=security_token,
            table_name=table_name,
            prefix=prefix,
            execution_date=execution_date,
            connection=connection
        )
        sales_force.download(limit=limit)
    else:
        LoggingMixin().log.error(f'SalesForce credentials not available for {instance} in config_default.yaml')
        raise AttributeError(f'SalesForce credentials not available for {instance} in config_default.yaml')
