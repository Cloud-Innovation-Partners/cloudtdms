#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import yaml
import os
import pandas as pd
from system.dags import get_output_data_home, get_config_default_path, get_user_data_home
from system.cloudtdms.extras import SOURCE_DOWNLOAD_LIMIT
from airflow.utils.log.logging_mixin import LoggingMixin


class CTDMS2CSV:
    def __init__(self, connection, source_file, execution_date, prefix, delimiter=","):
        self.connection = connection
        self.source_file = source_file
        self.execution_date = execution_date
        self.prefix = prefix
        self.delimiter = delimiter

    def download(self, limit=SOURCE_DOWNLOAD_LIMIT):
        file_name = f"csv_{self.connection}_{os.path.dirname(self.prefix)}_{os.path.basename(self.prefix)}_{str(self.execution_date)[:19].replace('-', '_').replace(':', '_')}.csv"
        extension = os.path.splitext(self.source_file)[1]
        if str(extension).lower() != '.csv':
            raise Exception(f"InvalidFileFormat: File {self.source_file} has no .csv extension")
        df = pd.read_csv(f"{get_user_data_home()}/{os.path.splitext(self.source_file)[0]}.csv", nrows=SOURCE_DOWNLOAD_LIMIT, sep=self.delimiter)
        df.columns = [f"csv.{self.connection}.{str(f).replace(' ','_')}" for f in df.columns]

        df.to_csv(f"{get_user_data_home()}/{file_name}", index=False)

    @staticmethod
    def get_csv_config_default():
        config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
        if config is not None and config.get('csv', None) is not None:
            return config.get('csv')
        else:
            raise KeyError('config_default.yaml has no csv entry')


def csv_upload(**kwargs):
    pass


def csv_download(**kwargs):
    execution_date = kwargs.get('execution_date', None)  # dag execution date
    prefix = kwargs.get('prefix')  # title of the synthetic data config file
    delimiter = kwargs.get('delimiter', ',') if kwargs.get('delimiter') != "" else ','
    connection = kwargs.get('connection')
    # Get CSV source file From config_default.yaml
    csv_config = CTDMS2CSV.get_csv_config_default()

    source_file = csv_config.get(connection).get('file', None)

    if source_file is not None:
        csv = CTDMS2CSV(
            connection=connection,
            source_file=source_file,
            prefix=prefix,
            delimiter=delimiter,
            execution_date=execution_date
        )
        csv.download()
    else:
        LoggingMixin().log.error(f'CSV file not available for {connection} in config_default.yaml')
        raise AttributeError(f'CSV file not available for {connection} in config_default.yaml')

