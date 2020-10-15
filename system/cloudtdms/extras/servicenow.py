
import base64
import requests
import os
import json
import ijson
import tempfile
import io
import yaml
import pandas as pd
from datetime import datetime
from airflow.utils.log.logging_mixin import LoggingMixin
from system.dags import get_output_data_home, get_config_default_path, get_user_data_home
from system.cloudtdms.extras import DESTINATION_UPLOAD_LIMIT, SOURCE_DOWNLOAD_LIMIT


class CTDMS2ServiceNow:

    def __init__(self, instance, username, password, table_name, prefix, execution_date):
        self.service_now_instance = instance
        self.service_now_username = username
        self.service_now_password = password
        self.name = str(table_name).upper()
        self.table_name = table_name
        self.file_prefix = prefix
        self.data = None
        self.execution_date = execution_date
        self.file_name = f"{os.path.basename(prefix)}_{str(execution_date)[:19].replace('-','_').replace(':','_')}.csv"

    def upload(self):
        """
        This is a convenience function used to upload the data
        :return:
        """
        synthetic_data_path = f"{get_output_data_home()}/{self.file_prefix}/{self.file_name}"
        if os.path.exists(synthetic_data_path):
            # TODO-Check If file is JSON or csv
            df = pd.read_csv(f"{synthetic_data_path}", nrows=DESTINATION_UPLOAD_LIMIT)
            a = df.to_json(lines=True, orient='records')
            objects = (json.loads(f) for f in io.StringIO(a).readlines())
            self.data = json.dumps({"records": list(objects)})

            authorization = base64.b64encode(
                str(base64.b64decode(str(self.service_now_username).encode()).decode('utf-8') + ":" +
                    base64.b64decode(str(self.service_now_password).encode()).decode('utf-8')).encode()
            ).decode()
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Authorization': 'Basic {}'.format(authorization)
            }

            LoggingMixin().log.info("[{}] API request start time {}".format(self.name, datetime.now()))

            response = requests.request("POST",
                                        url="https://{}.service-now.com/{}.do?JSONv2".format(self.service_now_instance,
                                                                                             self.table_name),
                                        params={"sysparm_action": "insertMultiple", },
                                        headers=headers,
                                        data=self.data,
                                        )
            # Throw an error for Bad Status Code
            response.raise_for_status()
            LoggingMixin().log.info("[{}] API request end time {}".format(self.name, datetime.now()))

            # TODO - Handle ServiceNow response exceptions

            response = None  # release
        else:
            LoggingMixin().log.error(f"No Synthetic Data Found @ {synthetic_data_path}!")
            raise FileNotFoundError

    def download(self, limit=SOURCE_DOWNLOAD_LIMIT):
        """
        This is a convenience function used to download the data
        :return:
        """
        authorization = base64.b64encode(
            str(base64.b64decode(str(self.service_now_username).encode()).decode('utf-8') + ":" +
                base64.b64decode(str(self.service_now_password).encode()).decode('utf-8')).encode()
        ).decode()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Authorization': 'Basic {}'.format(authorization)
        }

        LoggingMixin().log.info("[{}] API request start time {}".format(self.name, datetime.now()))
        response = requests.request("GET",
                                    url="https://{}.service-now.com/api/now/table/{}?".format(self.service_now_instance, self.table_name),
                                    params={
                                        "sysparm_query": "active=true^ORDERBYDESCsys_updated_on",
                                        "sysparm_limit": "{}".format(limit)
                                    },
                                    headers=headers,
                                    stream=True
                                    )
        # Throw an error for Bad Status Code
        response.raise_for_status()

        df = None
        with tempfile.NamedTemporaryFile('rb+') as f:
            f.seek(0)
            for block in response.iter_content(1024):
                f.write(block)
            f.seek(0)
            objects = ijson.items(f, 'result.item')
            records = [o for o in objects]
            df = pd.DataFrame(records)

        file_name = f"{os.path.basename(self.file_prefix)}_{str(self.execution_date)[:19].replace('-','_').replace(':','_')}.csv"

        df.to_csv(f'{get_user_data_home()}/{file_name}', index=False)

        LoggingMixin().log.info("[{}] API request end time {}".format(self.name, datetime.now()))

        # TODO - Handle ServiceNow response exceptions

        response = None  # release

    @staticmethod
    def get_service_now_config_default():
        config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
        if config is not None and config.get('servicenow', None) is not None:
            return config.get('servicenow')
        else:
            raise KeyError('config_default.yaml has no servicenow entry')


def service_now_upload(**kwargs):

    execution_date = kwargs.get('execution_date', None)     # dag execution date
    table_name = kwargs.get('table_name')       # ServiceNow table name
    prefix = kwargs.get('prefix')       # title of the synthetic data config file
    instance = kwargs.get('instance')
    # Load ServiceNow Instance From config_default.yaml
    service_now_config = CTDMS2ServiceNow.get_service_now_config_default()

    username = service_now_config.get(instance).get('username', None)
    password = service_now_config.get(instance).get('password', None)

    if username is not None and password is not None:
        service_now = CTDMS2ServiceNow(
            instance=instance,
            username=username,
            password=password,
            table_name=table_name,
            prefix=prefix,
            execution_date=execution_date
        )
        service_now.upload()
    else:
        LoggingMixin().log.error(f'ServiceNow credentials not available for {instance} in config_default.yaml')


def service_now_download(**kwargs):
    execution_date = kwargs.get('execution_date', None)  # dag execution date
    table_name = kwargs.get('table_name')  # ServiceNow table name
    prefix = kwargs.get('prefix')  # title of the synthetic data config file
    instance = kwargs.get('instance')
    limit = kwargs.get('limit') if kwargs.get('limit') != "" else 5000
    # Load ServiceNow Instance From config_default.yaml
    service_now_config = CTDMS2ServiceNow.get_service_now_config_default()

    username = service_now_config.get(instance).get('username', None)
    password = service_now_config.get(instance).get('password', None)

    if username is not None and password is not None:
        service_now = CTDMS2ServiceNow(
            instance=instance,
            username=username,
            password=password,
            table_name=table_name,
            prefix=prefix,
            execution_date=execution_date
        )
        service_now.download(limit=limit)
    else:
        LoggingMixin().log.error(f'ServiceNow credentials not available for {instance} in config_default.yaml')
        raise AttributeError(f'ServiceNow credentials not available for {instance} in config_default.yaml')
