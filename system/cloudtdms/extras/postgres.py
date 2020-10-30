#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import base64
import itertools
import os

import psycopg2
import psycopg2.extras
import psycopg2 as pg
import sqlalchemy
import yaml
from sqlalchemy.pool import NullPool

from system.dags import get_config_default_path, get_output_data_home, get_user_data_home
from airflow.utils.log.logging_mixin import LoggingMixin
import pandas as pd
from sqlalchemy import create_engine
from pandas.io import sql
from system.cloudtdms.extras import SOURCE_DOWNLOAD_LIMIT
import numpy
from psycopg2.extensions import register_adapter, AsIs

valid_dbs = {}


def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)

def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

def addapt_numpy_bool(numpy_bool):
    return AsIs(numpy_bool)

register_adapter(numpy.float64, addapt_numpy_float64)

register_adapter(numpy.int64, addapt_numpy_int64)

register_adapter(numpy.bool_, addapt_numpy_bool)

def get_postgres_config_default():
    config = yaml.load(open(get_config_default_path()), Loader=yaml.FullLoader)
    if config is not None and config.get('postgres', None) is not None:
        return config.get('postgres')
    else:
        raise KeyError('config_default.yaml has no postgres entry')


# [{'connection': 'mssql_dev', 'table': 'incident'}, {'connection': 'mssql_prod', 'table': 'incident2'}]
def validate_mysql_credentials(database_list):
    mssql_config = get_postgres_config_default()
    for db in database_list:
        if db['connection'] not in mssql_config:
            raise AttributeError(f"{db['connection']} not found in config_default.yaml")
        if len(mssql_config[db['connection']]['host'].split('.')) != 4:
            raise ValueError(f"Host in {db['connection']} database has in-valid format in config_default.yaml")

        valid_dbs[db['connection']] = db['table']


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


def get_sub_query(column_names):
    """This method returns a query """
    # 'CREATE TABLE ABC (name varchar(50), address varchar(50))'
    query = 'id SERIAL PRIMARY KEY, '
    dtype = 'VARCHAR(255), '
    for col in column_names:
        table_column = col + ' ' + dtype
        query += table_column

    query = query.strip().strip(',')
    return query


# MAIN FUNCTION #
def postgres_upload(**kwargs):
    connection_name = kwargs['connection']
    prefix = kwargs['prefix']
    execution_date = kwargs['execution_date']
    table_name = kwargs['table_name']
    file_name = f"{os.path.basename(kwargs['prefix'])}_{str(kwargs['execution_date'])[:19].replace('-', '_').replace(':', '_')}.csv"

    # validate_mysql_credentials(kwargs['database'])

    connection_in_yaml = get_postgres_config_default()

    # read latest modified csv file
    latest_file_path = get_output_data_home() + '/' + kwargs['prefix'] + '/' + file_name
    LoggingMixin().log.info(f" LATEST FILE PATH : {latest_file_path}")
    csv_file = pd.read_csv(latest_file_path)

    is_available = True if connection_name in connection_in_yaml else False

    if is_available:
        database = connection_in_yaml.get(connection_name).get('database')
        user = decode_(connection_in_yaml.get(connection_name).get('username')).replace('\n', '')
        password = decode_(connection_in_yaml.get(connection_name).get('password')).replace('\n', '')
        host = connection_in_yaml.get(connection_name).get('host').replace(' ', '')
        port = int(connection_in_yaml.get(connection_name).get('port')) if connection_in_yaml.get(connection_name).get(
            'port') else 5432

        LoggingMixin().log.info(f'Inserting data in {database}, {table_name}')
        engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}", poolclass=NullPool)

        # store the data in the database
        n_objects = Converter.df_to_gen(csv_file)
        storage = Storage(user, password, host, database, table_name, port)

        if storage.has_table(str(table_name).lower(), engine):
            LoggingMixin().log.info(f"Table {table_name} already existed")
            # 'check_schema'
            schema_values = storage.is_schema_changed(str(table_name).lower(), engine, list(csv_file.columns))
            is_changed = schema_values[0]
            new_cols = schema_values[1]
            LoggingMixin().log.info(f'New cols: {new_cols}')
            if is_changed:  # schema changed
                LoggingMixin().log.info(f"Schema of table {str(table_name).lower()} in {database} changed")
                storage.modify_table(str(table_name).lower(), new_cols)
                storage.insert_data(n_objects)
            else:
                LoggingMixin().log.info(f"Schema of table {str(table_name).lower()} not changed, appending new records")
                storage.insert_data(n_objects)
        else:
            storage.create_table(list(csv_file.columns))
            storage.insert_data(n_objects)
    else:
        raise AttributeError(f"{connection_name} not found in config_default.yaml")


def postgres_download(**kwargs):
    connection_name = kwargs['connection']
    table_name = kwargs['table_name']
    execution_date = kwargs['execution_date']
    prefix = kwargs['prefix']

    connection_in_yaml = get_postgres_config_default()

    database = connection_in_yaml.get(connection_name).get('database')
    username = decode_(connection_in_yaml.get(connection_name).get('username'))
    password = decode_(connection_in_yaml.get(connection_name).get('password'))
    host = connection_in_yaml.get(connection_name).get('host') if connection_in_yaml.get(connection_name).get(
        'host') else None
    port = int(connection_in_yaml.get(connection_name).get('port')) if connection_in_yaml.get(connection_name).get(
        'port') else 5432

    if host is not None:
        connection = pg.connect(
            host=host,
            user=username.replace('\n', ''),
            password=password.replace('\n', ''),
            database=database,
            port=port
        )

        file_name = f"postgres_{connection_name}_{os.path.dirname(prefix)}_{os.path.basename(prefix)}_{str(execution_date)[:19].replace('-', '_').replace(':', '_')}.csv"
        try:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                # Get PRIMARY INDEX column
                sql = f"""
                     SELECT column_name
                        FROM information_schema.table_constraints
                             JOIN information_schema.key_column_usage
                                 USING (constraint_catalog, constraint_schema, constraint_name,
                                        table_catalog, table_schema, table_name)
                        WHERE constraint_type = 'PRIMARY KEY'
                          AND (table_schema, table_name) = ('public', '{table_name}')
                        """
                cursor.execute(sql)
                result = cursor.fetchone()  # result contains tuple- ('id', )
                primary_index = result['column_name'] if result is not None else None

                if primary_index is not None:
                    sql = f"SELECT * FROM {table_name} ORDER BY {primary_index} DESC LIMIT {SOURCE_DOWNLOAD_LIMIT}"
                    cursor.execute(sql)
                    df = pd.DataFrame(cursor.fetchall())
                    df.columns = [f"postgres.{connection_name}.{table_name}.{f}" for f in df.columns]

                else:
                    LoggingMixin().log.warn(
                        f"Database table {database}.{table_name} has no INDEX column defined, Latest Records will not be fetched!")
                    sql = f"SELECT * FROM {table_name} LIMIT {SOURCE_DOWNLOAD_LIMIT}"
                    cursor.execute(sql)
                    df = pd.DataFrame(cursor.fetchall())
                    df.columns = [f"postgres.{connection_name}.{table_name}.{f}" for f in df.columns]

                try:
                    df.to_csv(f'{get_user_data_home()}/.__temp__/{file_name}', index=False)
                except FileNotFoundError:
                    os.makedirs(f'{get_user_data_home()}/.__temp__/')
                    df.to_csv(f'{get_user_data_home()}/.__temp__/{file_name}', index=False)

        finally:
            connection.close()
    else:
        LoggingMixin().log.error(f"NoHostFound: No host was found for database {database}")


class Converter():

    @staticmethod
    def df_to_gen(csv_file):
        yield tuple(csv_file.columns)
        for i in range(len(csv_file)):
            yield tuple(csv_file.iloc[i])


class Storage():
    """
    This class takes the MySql credentials and creates a connection with MySql database
    """

    def __init__(self, login, password, host, database_name, table_name, port):
        self.login = login
        self.password = password
        self.host = host
        self.database_name = database_name
        self.table_name = str(table_name).lower()
        self.port = port

    def has_table(self, table, engine):
        """This methods check whether the table is already present in database"""
        return sql.has_table(table, con=engine)

    def is_schema_changed(self, table, engine, csv_cols):
        """This methods check whether the schema of table is changed or not"""
        table_schema = sql.read_sql(sql=f"SELECT * from {table} LIMIT 1", con=engine)
        new_cols = get_new_columns(list(table_schema.columns), csv_cols)
        new_cols = [i for i in new_cols if i != 'id']  # id column is already present in database, so remove it
        return len(new_cols) != 0, new_cols

    def modify_table(self, table, new_cols):
        """This methods modifies the table present in database for which schema is changed"""
        conn = pg.connect(host=self.host, user=self.login, password=self.password,
                          port=self.port, database=self.database_name)
        cursor = conn.cursor()
        for col in new_cols:
            try:
                alter_query = f'ALTER TABLE {table} ADD {col} VARCHAR(255);'
                LoggingMixin().log.info(f'ALTER QUERY {alter_query}')
                cursor.execute(alter_query)
                conn.commit()
            except (psycopg2.errors.DuplicateColumn, psycopg2.errors.InFailedSqlTransaction):
                LoggingMixin().log.info(f'{col} already existed, Alter command cannot be executed...')
        conn.close()

    def create_table(self, column_names):
        """
            This method creates the table in the database(database name is specified in the parameter
            self.database_name )
            -create columns for all labels, including the extra one on schema
            """
        conn = pg.connect(host=self.host, user=self.login, password=self.password,
                          port=self.port, database=self.database_name)
        cursor = conn.cursor()
        sub_query = get_sub_query(column_names)
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
        conn = pg.connect(host=self.host, user=self.login, password=self.password,
                          database=self.database_name)
        cursor = conn.cursor()

        cols = next(n_objects)  # inital record in n_objects will be column names, see Converter.df_to_gen()
        column_names = list(cols)
        placeholders = ''.join("%s," * len(column_names))
        placeholders = placeholders.strip(',')
        column_names = ",".join(column_names)

        sql = "INSERT INTO {} ({}) VALUES ({})".format(self.table_name, column_names, placeholders)
        print(f"INSERT QUERY: {sql} ")
        # insert second_record, first_record is column names
        cursor.execute(sql, next(n_objects))
        conn.commit()

        while True:  # traverse to the end of the generator object
            itr = itertools.islice(n_objects, 0, step)
            for i in itr:
                lst.append(i)
            # print(lst)
            if not lst:  # check for lst is empty, if empty that means end of generator is reached.
                break
            cursor.executemany(sql, lst)
            conn.commit()
            lst.clear()
        conn.close()
