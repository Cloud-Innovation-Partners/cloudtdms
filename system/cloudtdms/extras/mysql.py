#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import os
import yaml
from system.dags import get_config_default_path, get_output_data_home
import pandas as pd
from sqlalchemy import create_engine

def get_mysql_config_default():
    config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
    if config is not None and config.get('mysql', None) is not None:
        return config.get('mysql')
    else:
        raise KeyError('config_default.yaml has no mysql entry')

def validate_mysql_credentials(database_list):
    mysql_config=get_mysql_config_default()
    for db in database_list:
        if db['name'] not in mysql_config:
            raise AttributeError(f"{db['name']} not found in config_default.yaml")

def all_files_under(file_path):
    files=os.listdir(file_path)
    for filename in files:
        yield os.path.join(file_path, filename)



def upload(**kwargs): #{'folder_title':'test_storages', 'databases': [{'name': 'dev', 'table': 'incident'}, {'name': 'prod', 'table': 'incident2'}]}
    validate_mysql_credentials(kwargs['databases'])

    connections=get_mysql_config_default()

    #read csv file
    file_path=get_output_data_home()+'/'+kwargs['folder_title']
    latest_file_path = max(all_files_under(file_path), key=os.path.getmtime)
    csv_file=pd.read_csv(latest_file_path)

    for db_name in connections:

        user=connections[db_name]['username']
        password=connections[db_name]['password']
        host=connections[db_name]['host']

        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")#mysql+pymysql://user:password@localhost/database"
        csv_file.to_sql(con=engine, name=connections[db_name]['table_name'], if_exists='replace', index = False)
