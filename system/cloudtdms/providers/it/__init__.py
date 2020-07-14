#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from faker import Faker
from faker.providers import internet
from faker.providers import misc
from airflow.utils.log.logging_mixin import LoggingMixin


def ip_address(number, args):
    """
    Generator function for ip address
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    category = args['category']
    fake = Faker()
    fake.add_provider(internet)
    if category == 'v4':
        return list([fake.ipv4() for _ in range(int(number))])
    elif category == 'v6':
        return list([fake.ipv6() for _ in range(int(number))])
    else:
        LoggingMixin().log.warning(f"InvalidAttribute: Invalid `category` = {category} value found!")
        return list([fake.ipv4() for _ in range(int(number))])


def mac_address(number, args):
    """
    Generator function for MAC Address
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    fake = Faker()
    fake.add_provider(internet)
    return list([fake.mac_address() for _ in range(int(number))])


def sha1(number, args):
    """
    Generator function for SHA1 hex string
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    fake = Faker()
    fake.add_provider(misc)
    return list([fake.sha1() for _ in range(int(number))])


def sha256(number, args):
    """
    Generator function for SHA1 hex string
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    fake = Faker()
    fake.add_provider(misc)
    return list([fake.sha256() for _ in range(int(number))])


def domain_name(number, args):
    """
    Generator function for Domain Names
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    fake = Faker()
    fake.add_provider(internet)
    return list([fake.domain_name() for _ in range(int(number))])
