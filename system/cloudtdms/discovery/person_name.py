#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

# Contains Search Rules for Identifying Person Name in User Data

import numpy as np
import pandas as pd
from functools import reduce
from system.dags import get_providers_home

sensitive_column_headers = ['first_name', 'last_name', 'fname', 'f_name', 'lname', 'l_name', 'surname', 'middle_name',
                            'family_name', 'sname', 's_name', 'forename', 'name', 'full_name', 'given_name',
                            'maiden_name', 'mname', 'g_name', 'm_name', 'initial_name', 'initial']


def search_on_column_basis(data_frame):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'Name', 'sensitvity': 'high', 'basis' : 'column_name'} for f in column_headers if f in sensitive_column_headers]
    return matched_columns


def search_on_data_basis(data_frame, matched):
    data_frame.drop(matched, inplace=True, axis=1)

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/personal/person.csv')
    statistic_match = []

    for column in columns:
        if len(df) > len(data_frame):
            f_mask = df['first_name'].isin(data_frame[column])
            l_mask = df['last_name'].isin(data_frame[column])
            total = sum(f_mask) + sum(l_mask)
            factor = total / (len(df)*2)
        else:
            f_mask = data_frame[column].isin(df['first_name'])
            l_mask = data_frame[column].isin(df['last_name'])
            total = sum(f_mask) + sum(l_mask)
            factor = total / (len(data_frame)*2)
        score = factor*100
        if score > 50:
            statistic_match.append({column: int(score),  'match': 'Name','sensitvity': 'high', 'basis': 'column_data'})

    return statistic_match


def search(data_frame):
    result = search_on_column_basis(data_frame)
    result += search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])

    return result