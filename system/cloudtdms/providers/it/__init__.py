#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from faker import Faker
from faker.providers import internet
from faker.providers import misc
from airflow.utils.log.logging_mixin import LoggingMixin


def it(data_frame, number, args):
    field_names = {}
    for k in args:
        if k.split('-$-', 2)[1] not in field_names:
            field_names[k.split('-$-', 2)[1]] = {k.split('-$-', 2)[0]: args.get(k)}
        else:
            field_names[k.split('-$-', 2)[1]][k.split('-$-', 2)[0]] = args.get(k)

    columns = field_names.keys()

    for col in columns:
        mod = globals()[col]
        mod(data_frame, number, field_names.get(col))


def ip_address(data_frame, number, args=None):
    """
    Generator function for ip address
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("ip_address")]
    for column_name, data_frame_col_name in zip(args, dcols):
        category = args.get(column_name).get('category', 'v4')
        fake = Faker()
        fake.add_provider(internet)
        if category == 'v4':
            data_frame[data_frame_col_name] = list([fake.ipv4() for _ in range(int(number))])
        elif category == 'v6':
            data_frame[data_frame_col_name] = list([fake.ipv6() for _ in range(int(number))])
        else:
            LoggingMixin().log.warning(f"InvalidAttribute: Invalid `category` = {category} value found!")
            data_frame[data_frame_col_name] = list([fake.ipv4() for _ in range(int(number))])
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def mac_address(data_frame, number, args=None):
    """
    Generator function for MAC Address
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("mac_address")]
    for column_name, data_frame_col_name in zip(args, dcols):
        fake = Faker()
        fake.add_provider(internet)
        data_frame[data_frame_col_name] = list([fake.mac_address() for _ in range(int(number))])
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def sha1(data_frame, number, args=None):
    """
    Generator function for SHA1 hex string
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("sha1")]
    for column_name, data_frame_col_name in zip(args, dcols):
        fake = Faker()
        fake.add_provider(misc)
        data_frame[data_frame_col_name] = list([fake.sha1() for _ in range(int(number))])
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def sha256(data_frame, number, args=None):
    """
    Generator function for SHA1 hex string
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("sha256")]
    for column_name, data_frame_col_name in zip(args, dcols):
        fake = Faker()
        fake.add_provider(misc)
        data_frame[data_frame_col_name] = list([fake.sha256() for _ in range(int(number))])
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def domain_name(data_frame, number, args=None):
    """
    Generator function for Domain Names
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("domain_name")]
    for column_name, data_frame_col_name in zip(args, dcols):
        fake = Faker()
        fake.add_provider(internet)
        data_frame[data_frame_col_name] = list([fake.domain_name() for _ in range(int(number))])
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)
