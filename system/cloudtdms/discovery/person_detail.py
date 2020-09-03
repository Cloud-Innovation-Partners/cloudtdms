#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

# Contains Search Rules for Identifying Person Details in User Data

import numpy as np
import pandas as pd
import re
from functools import reduce
#from airflow.utils.log.logging_mixin import LoggingMixin

age_sensitive_column_headers = ['age', 'maturity', 'seniority', 'years', 'duration', 'age_group', 'oldness']
gender_sensitive_column_headers = ['gender', 'sex', 'kind', 'sexuality', 'male', 'female', 'identity', 'neuter']
email_sensitive_column_headers = ['email', 'mail', 'e-mail', 'message', 'electronic_mail', 'post', 'correspondence',
                                  'send', 'mailing', 'memo', 'mailbox', 'write']


def age_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [f for f in column_headers if f in age_sensitive_column_headers]
    return matched_columns


def gender_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [f for f in column_headers if f in gender_sensitive_column_headers]
    return matched_columns


def email_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [f for f in column_headers if f in email_sensitive_column_headers]
    return matched_columns


def gender_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")


    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    df_1 = pd.DataFrame({'gender':['male', 'female']})
    df_2 = pd.DataFrame({'gender':['m','f']})
    df_3 = pd.DataFrame({'gender':['Male', 'Female']})
    df_4 = pd.DataFrame({'gender':['M','F']})
    statistic_match = []

    for column in columns:
        df_1_intersection = reduce(np.intersect1d, [data_frame[column], df_1['gender']])
        df_2_intersection = reduce(np.intersect1d, [data_frame[column], df_2['gender']])
        df_3_intersection = reduce(np.intersect1d, [data_frame[column], df_3['gender']])
        df_4_intersection = reduce(np.intersect1d, [data_frame[column], df_4['gender']])
        if len(df_1_intersection) == 2 or len(df_2_intersection) == 2\
                or len(df_3_intersection) == 2 or len(df_4_intersection) == 2:
            statistic_match.append(column)

    return statistic_match


def age_search_on_data_basis(data_frame, matched):
    data_frame.drop(matched, inplace=True, axis=1)
    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == int).all(0)]]
    columns = data_frame.columns

    # Load Sample Data
    df = pd.DataFrame({'age': range(18, 81)})
    statistic_match = []

    for column in columns:
        age_intersection = reduce(np.intersect1d, [data_frame[column], df['age']])
        if len(age_intersection) >= 63:
            statistic_match.append(column)

    return statistic_match


def email_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    r = re.compile(regex)
    for column in columns:
        mask = data_frame[column].apply(lambda x: bool(r.match(x)))
        if mask.sum() > 100:
            statistic_match.append(column)

    return statistic_match


def search(data_frame):
    result = []
    result += age_search_on_column_basis(data_frame, result)
    result += gender_search_on_column_basis(data_frame, result)
    result += email_search_on_column_basis(data_frame, result)
    result += age_search_on_data_basis(data_frame, result)
    result += email_search_on_data_basis(data_frame, result)
    result += gender_search_on_data_basis(data_frame, result)

    return result