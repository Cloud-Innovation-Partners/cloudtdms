#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

# Contains Search Rules for Identifying Person Name in User Data

import pandas as pd
import re
from system.dags import get_providers_home

sensitive_column_headers = ['first_name', 'last_name', 'fname', 'f_name', 'lname', 'l_name', 'surname', 'middle_name',
                            'family_name', 'sname', 's_name', 'forename', 'name', 'full_name', 'given_name',
                            'maiden_name', 'mname', 'g_name', 'm_name', 'initial_name', 'initial', 'firstname', 'FirstName'
                            'lastname', 'LastName', 'customer']


def lexeme_search(token: str, searchable: list):
    tokens = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', token)
    mask = map(lambda x: True if str(x).lower() in searchable else False, tokens)
    return any(mask)


def search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, sensitive_column_headers) else 0, data_frame.columns)
    return score


def search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/personal/person.csv', usecols=['first_name', 'last_name'])
    name = pd.DataFrame(df['first_name'].append(df['last_name']), columns=['name'])

    statistic_match = []

    for column in columns:
        if data_frame[column].dtype == 'object':
            mask = data_frame[column].isin(name['name'])
            total = sum(mask)
            factor = total / (len(data_frame))
            score = factor*100
            statistic_match.append(int(score))
        else:
            statistic_match.append(0)

    return statistic_match


def search(data_frame, pii_scale: callable):
    name_scores = list(map(pii_scale, search_on_column_basis(data_frame), search_on_data_basis(data_frame)))
    result = [{data_frame.columns[i]: round(name_scores[i], 1), 'match': 'Name', 'sensitivity': 'high', 'basis': 'pii_scale'}
              for i in range(len(data_frame.columns)) if name_scores[i] > 10.0]
    return result
