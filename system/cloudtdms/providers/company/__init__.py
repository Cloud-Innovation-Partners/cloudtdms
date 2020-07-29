#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os
import random
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin


def company(data_frame, number, args):
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

def company_name(data_frame, number, args=None):
    """
    Generator function for company names
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """

    dcols = [f for f in data_frame.columns if f.startswith("company_name")]
    for column_name, data_frame_col_name in zip(args, dcols):
        locale = args.get('locale', 'en_GB')
        df = pd.read_csv(f"{os.path.dirname(__file__)}/{locale}/d_company.csv", usecols=['company_name'])
        data_frame[data_frame_col_name] = [df.iloc[random.randint(0, len(df)-1)]['company_name'] for _ in range(int(number))]
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)

def department(data_frame, number, args=None):
    """
     Generator function for department
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """


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
    dcols = [f for f in data_frame.columns if f.startswith("department")]
    for column_name, data_frame_col_name in zip(args, dcols):
        category = args.get(column_name).get('category', 'corporate')
        if category is 'retail':
            data_frame[data_frame_col_name] = [_retail_[i % len(_retail_)] for i in range(int(number))]
        elif category is 'corporate':
            data_frame[data_frame_col_name] =  [_corporate_[i % len(_corporate_)] for i in range(int(number))]
        else:
            LoggingMixin().log.warning(f"InvalidAttribute: Invalid `category` = {category} value found!")
            data_frame[data_frame_col_name] =  [_corporate_[i % len(_retail_)] for i in range(int(number))]

        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def duns_number(data_frame, number, args=None):
    """
     Generator function for DUNS Number
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """

    duns_format = "##-###-####"
    dcols = [f for f in data_frame.columns if f.startswith("duns_number")]
    for column_name, data_frame_col_name in zip(args, dcols):
        data_frame[data_frame_col_name] = [
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
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)
