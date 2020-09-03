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
    matched_columns = [f for f in column_headers if f in sensitive_column_headers]
    return matched_columns


def search_on_data_basis(data_frame, matched):
    data_frame.drop(matched, inplace=True, axis=1)

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/personal/person.csv')
    statistic_match = []

    for column in columns:
        f_intersection = reduce(np.intersect1d, [data_frame[column], df['first_name']])
        l_intersection = reduce(np.intersect1d, [data_frame[column], df['last_name']])
        if len(f_intersection) > 100 or len(l_intersection) > 100:
            statistic_match.append(column)

    return statistic_match


def search(data_frame):
    result = search_on_column_basis(data_frame)
    result += search_on_data_basis(data_frame, result)

    return result