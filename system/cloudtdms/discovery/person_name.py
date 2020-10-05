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
    df = pd.read_csv(f'{get_providers_home()}/personal/person.csv', usecols=['first_name', 'last_name'])
    name = pd.DataFrame(df['first_name'].append(df['last_name']), columns=['name'])

    statistic_match = []

    for column in columns:
        mask = data_frame[column].isin(name['name'])
        total = sum(mask)
        factor = total / (len(data_frame))
        score = factor*100
        if score >= 50:
            statistic_match.append({column: int(score),  'match': 'Name','sensitvity': 'high', 'basis': 'column_data'})

    return statistic_match


def search(data_frame):
    result = search_on_column_basis(data_frame)
    result += search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])

    return result