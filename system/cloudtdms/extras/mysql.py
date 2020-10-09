#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import base64
import os
import yaml
from system.dags import get_config_default_path, get_output_data_home
import pandas as pd
from sqlalchemy import create_engine

table_names={}

def get_mysql_config_default():
    config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
    if config is not None and config.get('mysql', None) is not None:
        return config.get('mysql')
    else:
        raise KeyError('config_default.yaml has no mysql entry')

def validate_mysql_credentials(database_list):
    mysql_config=get_mysql_config_default()
    for db in database_list:
        if db['connection'] not in mysql_config:
            raise AttributeError(f"{db['connection']} not found in config_default.yaml")
        if len(mysql_config[db['connection']]['host'].split('.')) !=4:
            raise ValueError(f"Host in {db['connection']} database has in-valid format in config_default.yaml")

        table_names[db['connection']]=db['table']


def all_files_under(file_path):
    files=os.listdir(file_path)
    for filename in files:
        yield os.path.join(file_path, filename)


def decode_(field):
    base64_bytes = field.encode("UTF-8")

    field_bytes = base64.b64decode(base64_bytes)
    decoded_field = field_bytes.decode("UTF-8")
    return  decoded_field



def upload(**kwargs): #{'folder_title':'test_storages', 'databases': [{'connection': 'dev', 'table': 'incident'}, {'connection': 'prod', 'table': 'incident2'}]}
    validate_mysql_credentials(kwargs['databases'])

    connection_in_yaml=get_mysql_config_default()

    #read latest modified csv file
    file_path=get_output_data_home()+'/'+kwargs['folder_title']
    latest_file_path = max(all_files_under(file_path), key=os.path.getmtime)
    csv_file=pd.read_csv(latest_file_path)

    for db_name in connection_in_yaml:

        user=decode_(connection_in_yaml[db_name]['username']).replace('\n','')
        password=decode_(connection_in_yaml[db_name]['password']).replace('\n','')
        host=connection_in_yaml[db_name]['host'].replace(' ','')
        table=table_names[db_name]

        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")#mysql+pymysql://user:password@localhost/database"
        csv_file.to_sql(con=engine, name=table, if_exists='replace', index = False)
