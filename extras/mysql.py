#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import os

import yaml
from system.dags import get_config_default_path, get_output_data_home
import itertools
import MySQLdb as ms
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
        # # store the data in the database
        # storage = Storage(connections[db_name]['username'], connections[db_name]['password'],
        #                   connections[db_name]['host'], db_name, connections[db_name]['table_name'],
        #                   connections[db_name]['port'])
        #
        # storage.create_table(csv_file.columns)
        # # storage.insert_data(n_objects)

        # #sotre data using pandas
        # conn = ms.connect(host=connections[db_name]['host'], user=connections[db_name]['username'],
        #                   password=connections[db_name]['password'],
        #                   port=int(connections[db_name]['port']), db=db_name)
        #
        # csv_file.to_sql(con=conn, name=connections[db_name]['table_name'], if_exists='replace', index = False)
        # conn.close()

        user=connections[db_name]['username']
        password=connections[db_name]['password']
        host=connections[db_name]['host']

        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")#mysql+pymysql://user:password@localhost/database"
        csv_file.to_sql(con=engine, name=connections[db_name]['table_name'], if_exists='replace', index = False)


class Storage():
    """
    This class takes the MySql credentials and creates a connection with MySql database
    """

    def __init__(self, login, password, host, database_name, table_name, port):
        self.login = login
        self.password = password
        self.host = host
        self.database_name = database_name
        self.table_name = table_name
        self.port = int(port)

    def create_table(self, column_names):
        """
        This method creates the table in the database(database name is specified in the parameter
        self.database_name )
        -create columns for all labels, including the extra one on schema
        """
        conn = ms.connect(host=self.host, user=self.login, password=self.password,
                          port=self.port, db=self.database_name)
        cursor = conn.cursor()
        # sub_query = get_query_with_col_size(column_names, size)
        sub_query=','.join("`" + col_name + "` varchar(100)" for col_name in column_names)
        #column_names = ','.join("`" + col_name + "` varchar(100)" for col_name in column_names)
        sql = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(self.table_name, sub_query)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def insert_data(self, n_objects):
        """
        This method inserts the parsed data(n_objects) in the MySql database
        insert data only for those columns which are present in the dict i.e n_objects
        """
        lst = []
        step = 100
        conn = ms.connect(host=self.host, user=self.login, password=self.password,
                          database=self.database_name)
        cursor = conn.cursor()

        intial_record = next(n_objects)
        column_names = list(intial_record.keys())
        placeholders = ''.join("%s," * len(column_names))
        placeholders = placeholders.strip(',')
        column_names = ",".join(column_names)

        sql = "INSERT INTO {} ({}) VALUES ({})".format(self.table_name, column_names, placeholders)
        # insert intial_record first
        cursor.execute(sql, tuple(intial_record.values()))
        conn.commit()

        while True:  # traverse to the end of the generator object
            itr = itertools.islice(n_objects, 0, step)
            for i in itr:
                lst.append(tuple(i.values()))
            # print(lst)
            if not lst:  # check for lst is empty, if empty that means end of generator is reached.
                break
            cursor.executemany(sql, lst)
            conn.commit()
            lst.clear()
        conn.close()