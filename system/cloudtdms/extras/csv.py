#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import yaml
import os
import pandas as pd
from system.dags import get_output_data_home, get_config_default_path, get_user_data_home
from system.cloudtdms.extras import SOURCE_DOWNLOAD_LIMIT, DESTINATION_UPLOAD_LIMIT
from airflow.utils.log.logging_mixin import LoggingMixin


class CTDMS2CSV:
    def __init__(self, connection, execution_date, prefix, source_file=None, target_file=None, delimiter=",",
                 header=True, quoting=False):
        self.connection = connection
        self.source_file = source_file
        self.target_file = target_file if (target_file is not None) and (len(target_file)!=0) else get_output_data_home()
        self.execution_date = execution_date
        self.prefix = prefix
        self.delimiter = delimiter
        self.header = header
        self.quoting = quoting

    def upload(self, limit=DESTINATION_UPLOAD_LIMIT):
        file_name = f"{os.path.basename(self.prefix)}_{str(self.execution_date)[:19].replace('-','_').replace(':','_')}.csv"
        synthetic_data_path = f"{get_output_data_home()}/{self.prefix}/{file_name}"
        if os.path.exists(synthetic_data_path):
            df = pd.read_csv(f"{synthetic_data_path}", nrows=int(DESTINATION_UPLOAD_LIMIT))

            # Drop Unnamed columns
            df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)

            try:
                LoggingMixin().log.info(
                    f"target_file : {os.path.splitext(self.target_file)[0]}/{self.prefix}/{file_name}")
                quoting_value = 1 if self.quoting else 0
                if self.header:
                    df.to_csv(f"{os.path.splitext(self.target_file)[0]}/{self.prefix}/{file_name}", index=False,
                              sep=str(self.delimiter), quoting=quoting_value)
                else:
                    df.to_csv(f"{os.path.splitext(self.target_file)[0]}/{self.prefix}/{file_name}", index=False,
                              sep=str(self.delimiter), header=False, quoting=quoting_value)
            except FileNotFoundError:
                os.makedirs(f"{os.path.splitext(self.target_file)[0]}/{self.prefix}")
                if self.header:
                    df.to_csv(f"{os.path.splitext(self.target_file)[0]}/{self.prefix}/{file_name}", index=False,
                              sep=str(self.delimiter), quoting=quoting_value)
                else:
                    df.to_csv(f"{os.path.splitext(self.target_file)[0]}/{self.prefix}/{file_name}", index=False,
                              sep=str(self.delimiter), header=False, quoting=quoting_value)
        else:
            LoggingMixin().log.error(f"No Synthetic Data Found @ {synthetic_data_path}!")
            raise FileNotFoundError

    def download(self, limit=SOURCE_DOWNLOAD_LIMIT):
        file_name = f"csv_{self.connection}_{os.path.dirname(self.prefix)}_{os.path.basename(self.prefix)}_{str(self.execution_date)[:19].replace('-', '_').replace(':', '_')}.csv"
        extension = os.path.splitext(self.source_file)[1]
        if str(extension).lower() != '.csv':
            raise Exception(f"InvalidFileFormat: File {self.source_file} has no .csv extension")
        if os.path.exists(self.source_file):
            df = pd.read_csv(f"{self.source_file}", engine='python', error_bad_lines=False,
                             nrows=SOURCE_DOWNLOAD_LIMIT, sep=self.delimiter)
        else:
            df = pd.read_csv(f"{get_user_data_home()}/{os.path.splitext(self.source_file)[0]}.csv", engine='python', error_bad_lines=False,
                             nrows=SOURCE_DOWNLOAD_LIMIT, sep=self.delimiter)

        df.columns = [f"csv.{self.connection}.{str(f).replace(' ','_')}" for f in df.columns]

        try:
            df.to_csv(f'{get_user_data_home()}/.__temp__/{file_name}', index=False)
        except FileNotFoundError:
            os.makedirs(f'{get_user_data_home()}/.__temp__/')
            df.to_csv(f'{get_user_data_home()}/.__temp__/{file_name}', index=False)

    @staticmethod
    def get_csv_config_default():
        config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
        if config is not None and config.get('csv', None) is not None:
            return config.get('csv')
        else:
            raise KeyError('config_default.yaml has no csv entry')


def csv_upload(**kwargs):
    execution_date = kwargs.get('execution_date', None)  # dag execution date
    prefix = kwargs.get('prefix')  # title of the synthetic data config file
    delimiter = kwargs.get('delimiter', ',') if kwargs.get('delimiter') != "" else ','
    connection = kwargs.get('connection')

    header = kwargs.get('header')
    header = True if str(header).lower() == 'true' else False

    quoting = kwargs.get('quoting')
    quoting = True if str(quoting).lower() == 'true' else False

    # Get CSV target file From config_default.yaml
    csv_config = CTDMS2CSV.get_csv_config_default()

    target_file = csv_config.get(connection).get('target', None)

    csv = CTDMS2CSV(
        connection=connection,
        target_file=target_file,
        prefix=prefix,
        delimiter=delimiter,
        execution_date=execution_date,
        header=header,
        quoting=quoting
    )
    csv.upload()


def csv_download(**kwargs):
    execution_date = kwargs.get('execution_date', None)  # dag execution date
    prefix = kwargs.get('prefix')  # title of the synthetic data config file
    delimiter = kwargs.get('delimiter', ',') if kwargs.get('delimiter') != "" else ','
    connection = kwargs.get('connection')
    # Get CSV source file From config_default.yaml
    csv_config = CTDMS2CSV.get_csv_config_default()

    source_file = csv_config.get(connection).get('source', None)

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