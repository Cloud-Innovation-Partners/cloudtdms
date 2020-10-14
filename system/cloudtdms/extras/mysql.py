#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import base64
import os

import sqlalchemy
import yaml
from system.dags import get_config_default_path, get_output_data_home
from airflow.utils.log.logging_mixin import LoggingMixin
import pandas as pd
from sqlalchemy import create_engine
from pandas.io import sql

table_names = {}


def get_mysql_config_default():
    config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
    if config is not None and config.get('mysql', None) is not None:
        return config.get('mysql')
    else:
        raise KeyError('config_default.yaml has no mysql entry')


# [{'connection': 'dev', 'table': 'incident'}, {'connection': 'prod', 'table': 'incident2'}]
def validate_mysql_credentials(database_list):
    mysql_config = get_mysql_config_default()
    for db in database_list:
        if db['connection'] not in mysql_config:
            raise AttributeError(f"{db['connection']} not found in config_default.yaml")
        if len(mysql_config[db['connection']]['host'].split('.')) != 4:
            raise ValueError(f"Host in {db['connection']} database has in-valid format in config_default.yaml")

        table_names[db['connection']] = db['table']


def all_files_under(file_path):
    files = os.listdir(file_path)
    for filename in files:
        yield os.path.join(file_path, filename)


def decode_(field):
    base64_bytes = field.encode("UTF-8")

    field_bytes = base64.b64decode(base64_bytes)
    decoded_field = field_bytes.decode("UTF-8")
    return decoded_field


def get_new_columns(schema_columns, csv_file_cols):
    s1s2 = set(schema_columns) - set(csv_file_cols)
    s2s1 = set(csv_file_cols) - set(schema_columns)
    new_cols = s1s2.union(s2s1)
    # if len(new_cols) is >0, means schema changed, 0 - schema not changed
    return new_cols


def get_alter_table_query(new_cols, table,sql, engine):
    # Alter Table Student ADD(Address Varchar(25), Phone INT, Email Varchar(20));
    alter_query = f'Alter Table `{table}` ADD('
    for col in new_cols:
        try:
            alter_query = f'Alter Table `{table}` ADD({col} Varchar(50));'
            LoggingMixin().log.info(f'ALTER QUERY {alter_query}')
            sql.execute(sql=alter_query, con=engine)
        except sqlalchemy.exc.OperationalError:
            LoggingMixin().log.info(f'{col} already existed, Alter command cannot be executed...')



def insert_data(new_cols, table, csv_file, engine):

    csv_columns=list(csv_file.columns)
    csv_columns=', '.join(csv_columns)
    for i in range(len(csv_file)):
        insert_query=f'INSERT INTO {table} ({csv_columns}) VALUES {tuple(csv_file.loc[i])};'
        LoggingMixin().log.info(insert_query)
        sql.execute(sql=insert_query, con=engine)




def mysql_upload(
        **kwargs):  # {'folder_title':'test_storages', 'databases': [{'connection': 'dev', 'table': 'incident'}, {'connection': 'prod', 'table': 'incident2'}]}
    validate_mysql_credentials(kwargs['databases'])

    connection_in_yaml = get_mysql_config_default()
    file_name= f"{os.path.basename(kwargs['prefix'])}_{str(kwargs['execution_date'])[:19].replace('-','_').replace(':','_')}.csv"

    # read latest modified csv file
    latest_file_path = get_output_data_home() + '/' + kwargs['folder_title']+'/'+file_name
    # latest_file_path = max(all_files_under(file_path), key=os.path.getmtime)
    LoggingMixin().log.info(f" LATEST FILE PATH : {latest_file_path}")
    csv_file = pd.read_csv(latest_file_path)

    for db_name in connection_in_yaml:
        user = decode_(connection_in_yaml[db_name]['username']).replace('\n', '')
        password = decode_(connection_in_yaml[db_name]['password']).replace('\n', '')
        host = connection_in_yaml[db_name]['host'].replace(' ', '')

        if db_name in table_names:  # check db_name(db in yaml file) present in scripts db's
            table = table_names[db_name]

            engine = create_engine(
                f"mysql+pymysql://{user}:{password}@{host}/{db_name}")  # mysql+pymysql://user:password@localhost/database"

            # check table exists, if exist, get schema
            if sql.has_table(table, con=engine):
                LoggingMixin().log.info(f'{table} existed')
                # new_schema = sql.get_schema(csv_file, table, con=engine)
                # LoggingMixin().log.info(f'New Schema {new_schema}')
                table_schema = sql.read_sql(sql=f"SELECT * FROM `{table}` LIMIT 1;", con=engine)
                new_cols = get_new_columns(list(table_schema.columns), list(csv_file.columns))

                if len(new_cols) > 0:  # schema changed
                    LoggingMixin().log.info(f'Schema of  {table} changed')
                    # alter_query = get_alter_table_query(new_cols, table)
                    # sql.execute(sql=alter_query, con=engine)
                    get_alter_table_query(new_cols,table,sql,engine)
                    insert_data(new_cols, table, csv_file, engine)
                else:
                    csv_file.to_sql(con=engine, name=table, if_exists='replace', index=False)

            else:
                csv_file.to_sql(con=engine, name=table, if_exists='replace', index=False)

