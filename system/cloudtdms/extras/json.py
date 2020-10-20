#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import yaml
import os
import pandas as pd
from system.dags import get_output_data_home, get_config_default_path, get_user_data_home
from system.cloudtdms.extras import SOURCE_DOWNLOAD_LIMIT
from airflow.utils.log.logging_mixin import LoggingMixin


class CTDMS2JSON:
    def __init__(self, connection, source_file, execution_date, prefix, type="lines"):
        self.connection = connection
        self.source_file = source_file
        self.execution_date = execution_date
        self.prefix = prefix
        self.type = type

    def download(self, limit=SOURCE_DOWNLOAD_LIMIT):
        file_name = f"json_{self.connection}_{os.path.dirname(self.prefix)}_{os.path.basename(self.prefix)}_{str(self.execution_date)[:19].replace('-', '_').replace(':', '_')}.csv"
        extension = os.path.splitext(self.source_file)[1]
        if str(extension).lower() != '.json':
            raise Exception(f"InvalidFileFormat: File {self.source_file} has no .json extension")
        if self.type == 'lines':
            df = pd.read_json(f"{get_user_data_home()}/{os.path.splitext(self.source_file)[0]}.json", nrows=SOURCE_DOWNLOAD_LIMIT, lines=True)
        elif self.type == 'array':
            df = pd.read_json(f"{get_user_data_home()}/{os.path.splitext(self.source_file)[0]}.json")
        else:
            raise ValueError("Unknown value for `type` attribute in json source")
        df.columns = [f"json.{self.connection}.{str(f).replace(' ','_')}" for f in df.columns]

        df.to_csv(f"{get_user_data_home()}/{file_name}", index=False)

    @staticmethod
    def get_json_config_default():
        config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
        if config is not None and config.get('json', None) is not None:
            return config.get('json')
        else:
            raise KeyError('config_default.yaml has no json entry')


def json_download(**kwargs):
    execution_date = kwargs.get('execution_date', None)  # dag execution date
    prefix = kwargs.get('prefix')  # title of the synthetic data config file
    type = kwargs.get('type', 'lines') if kwargs.get('type') != "" else 'lines'
    connection = kwargs.get('connection')
    # Get JSON source file From config_default.yaml
    json_config = CTDMS2JSON.get_json_config_default()

    source_file = json_config.get(connection).get('file', None)

    if source_file is not None:
        json = CTDMS2JSON(
            connection=connection,
            source_file=source_file,
            prefix=prefix,
            type=type,
            execution_date=execution_date
        )
        json.download()
    else:
        LoggingMixin().log.error(f'JSON file not available for {connection} in config_default.yaml')
        raise AttributeError(f'JSON file not available for {connection} in config_default.yaml')


def json_upload():
    pass
