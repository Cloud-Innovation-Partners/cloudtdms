#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import yaml
import os
import pandas as pd
from system.dags import get_output_data_home, get_config_default_path, get_user_data_home
from system.cloudtdms.extras import SOURCE_DOWNLOAD_LIMIT, DESTINATION_UPLOAD_LIMIT
from airflow.utils.log.logging_mixin import LoggingMixin
import xml.etree.ElementTree as ET


class Parser():
    """
    This class is actually responsible for parsing the xml data with the help of generators
    in a minimal possible time,  and creates an object for each parsed data
    """

    def __init__(self, file_path):
        self.file_path = file_path
        xml_data = open(self.file_path, 'r').read()  # Read file
        self.root = ET.XML(xml_data)  # Parse XML

    def get_column_labels(self):
        # get cols names only
        for i, child in enumerate(self.root):
            if i > 0:  # executes only one time, because we need only column names
                break
            cols = [subchild.tag for subchild in child]
        return cols

    def get_data(self):
        count = 0
        for i, child in enumerate(self.root):
            # if count == limit:
            #     break
            yield [subchild.text for subchild in child]
            # count += 1


def df_to_xml(file_path, df, root_tag, record_tag):
    def func(row):
        xml = [f'    <{record_tag}>']
        for field in row.index:
            xml.append('        <{0}>{1}</{0}>'.format(field, row[field]))
        xml.append(f'    </{record_tag}>')
        return '\n'.join(xml)

    with open(file_path, 'a') as f:
        f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        f.write(f"<{root_tag}>\n")
        data = '\n'.join(df.apply(func, axis=1))
        f.write(data)
        f.write(f"\n</{root_tag}>\n")


class CTDMS2XML:
    def __init__(self, connection, execution_date, prefix, source_file=None, target_file=None, root_tag='',
                 record_tag=''):
        self.connection = connection
        self.source_file = source_file
        self.target_file = target_file if (target_file is not None) and (
                len(target_file) != 0) else get_output_data_home()
        self.execution_date = execution_date
        self.prefix = prefix
        self.root_tag = root_tag
        self.record_tag = record_tag

    def upload(self, limit=DESTINATION_UPLOAD_LIMIT):
        file_name = f"{os.path.basename(self.prefix)}_{str(self.execution_date)[:19].replace('-', '_').replace(':', '_')}.csv"
        xml_file_name = f"{os.path.basename(self.prefix)}_{str(self.execution_date)[:19].replace('-', '_').replace(':', '_')}.xml"

        #delete csv file where xml file is created
        delete_csv_file_name =f"{os.path.basename(self.prefix)}_{str(self.execution_date)[:19].replace('-', '_').replace(':', '_')}.csv"

        synthetic_data_path = f"{get_output_data_home()}/{self.prefix}/{file_name}"
        if os.path.exists(synthetic_data_path):
            df = pd.read_csv(f"{synthetic_data_path}", nrows=int(DESTINATION_UPLOAD_LIMIT))

            # Drop Unnamed columns
            df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)

            try:
                LoggingMixin().log.info(
                    f"target_file : {os.path.splitext(self.target_file)[0]}/{self.prefix}/{xml_file_name}")
                # write df to xml
                # df.to_csv(f"{os.path.splitext(self.target_file)[0]}/{self.prefix}/{file_name}", index=False,)
                df_to_xml(file_path=f"{os.path.splitext(self.target_file)[0]}/{self.prefix}/{xml_file_name}", df=df,
                          root_tag=self.root_tag, record_tag=self.record_tag)

                # delete csv file where xml file is created
                delete_csv_file_path = f"{os.path.splitext(self.target_file)[0]}/{self.prefix}/{delete_csv_file_name}"
                if os.path.exists(delete_csv_file_path):
                    os.remove(delete_csv_file_path)

            except FileNotFoundError:
                os.makedirs(f"{os.path.splitext(self.target_file)[0]}/{self.prefix}")
                # write df to xml
                # df.to_csv(f"{os.path.splitext(self.target_file)[0]}/{self.prefix}/{file_name}", index=False)
                df_to_xml(file_path=f"{os.path.splitext(self.target_file)[0]}/{self.prefix}/{xml_file_name}", df=df,
                          root_tag=self.root_tag, record_tag=self.record_tag)

                # delete csv file where xml file is created
                delete_csv_file_path = f"{os.path.splitext(self.target_file)[0]}/{self.prefix}/{delete_csv_file_name}"
                if os.path.exists(delete_csv_file_path):
                    os.remove(delete_csv_file_path)
        else:
            LoggingMixin().log.error(f"No Synthetic Data Found @ {synthetic_data_path}!")
            raise FileNotFoundError

    def download(self, limit=SOURCE_DOWNLOAD_LIMIT):
        file_name = f"xml_{self.connection}_{os.path.dirname(self.prefix)}_{os.path.basename(self.prefix)}_{str(self.execution_date)[:19].replace('-', '_').replace(':', '_')}.csv"
        extension = os.path.splitext(self.source_file)[1]
        if str(extension).lower() != '.xml':
            raise Exception(f"InvalidFileFormat: File {self.source_file} has no .xml extension")

        # read xml file and convert into df
        # df = pd.read_csv(f"{self.source_file}", engine='python', error_bad_lines=False,
        #                      nrows=SOURCE_DOWNLOAD_LIMIT, sep=self.delimiter)
        parser = Parser(self.source_file)
        cols = parser.get_column_labels()
        data = parser.get_data()
        # load into df
        df = pd.DataFrame(data=data, columns=cols)

        df.columns = [f"xml.{self.connection}.{str(f).replace(' ', '_')}" for f in df.columns]
        # print(df)

        try:
            df.to_csv(f'{get_user_data_home()}/.__temp__/{file_name}', index=False)
        except FileNotFoundError:
            os.makedirs(f'{get_user_data_home()}/.__temp__/')
            df.to_csv(f'{get_user_data_home()}/.__temp__/{file_name}', index=False)

    @staticmethod
    def get_xml_config_default():
        config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
        if config is not None and config.get('xml', None) is not None:
            return config.get('xml')
        else:
            raise KeyError('config_default.yaml has no xml entry')


def xml_upload(**kwargs):
    execution_date = kwargs.get('execution_date', None)  # dag execution date
    prefix = kwargs.get('prefix')  # title of the synthetic data config file
    connection = kwargs.get('connection')
    root_tag = kwargs.get('root_tag', 'records')
    record_tag = kwargs.get('record_tag', 'record')

    # Get XML target file From config_default.yaml
    xml_config = CTDMS2XML.get_xml_config_default()

    target_file = xml_config.get(connection).get('target', None)

    xml = CTDMS2XML(
        connection=connection,
        target_file=target_file,
        prefix=prefix,
        execution_date=execution_date,
        root_tag=root_tag,
        record_tag=record_tag
    )
    xml.upload()


def xml_download(**kwargs):
    execution_date = kwargs.get('execution_date', None)  # dag execution date
    prefix = kwargs.get('prefix')  # title of the synthetic data config file
    connection = kwargs.get('connection')
    # Get XML source file From config_default.yaml
    xml_config = CTDMS2XML.get_xml_config_default()

    source_file = xml_config.get(connection).get('source', None)

    if source_file is not None:
        xml = CTDMS2XML(
            connection=connection,
            source_file=source_file,
            prefix=prefix,
            execution_date=execution_date
        )
        xml.download()
    else:
        LoggingMixin().log.error(f'XML file not available for {connection} in config_default.yaml')
        raise AttributeError(f'XML file not available for {connection} in config_default.yaml')
