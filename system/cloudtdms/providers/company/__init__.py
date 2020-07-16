#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os
import random
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin


def company_name(number, args=None):
    """
    Generator function for company names
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    df = pd.read_csv(f"{os.path.dirname(__file__)}/d_company.csv", usecols=['company_name'])
    return [df.iloc[i % len(df)]['company_name'] for i in range(int(number))]


def department(number, args=None):
    """
     Generator function for department
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    category = args.get('category', 'corporate')

    _corporate_ = ('Product Management',
                   'Research and Development',
                   'Business Development',
                   'Services',
                   'Engineering',
                   'Sales',
                   'Support',
                   'Training',
                   'Accounting',
                   'Legal',
                   'Human Resources',
                   'Marketing'
                   )

    _retail_ = (
        'Jewelery',
        'Grocery',
        'Home',
        'Kids',
        'Shoes',
        'Automotive',
        'Beauty',
        'Outdoors',
        'Computers',
        'Books',
        'Movies',
        'Baby',
        'Music',
        'Clothing',
        'Toys',
        'Tools',
        'Garden',
        'Electronics',
        'Industrial',
        'Health',
        'Games',
        'Sports'
    )

    if category is 'retail':
        return [_retail_[i % len(_retail_)] for i in range(int(number))]
    elif category is 'corporate':
        return [_corporate_[i % len(_corporate_)] for i in range(int(number))]
    else:
        LoggingMixin().log.warning(f"InvalidAttribute: Invalid `category` = {category} value found!")
        return [_corporate_[i % len(_retail_)] for i in range(int(number))]


def duns_number(number, args=None):
    """
     Generator function for DUNS Number
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """

    duns_format = "##-###-####"

    return [
        duns_format.replace("#", "{}").format(
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9)
        )
        for _ in range(int(number))]
