#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import pandas as pd
import numpy as np
from system.dags import get_providers_home
import re

latitude_sensitive_column_headers = ['latitude', 'altitude']
longitude_sensitive_column_headers = ['longitude']
country_sensitive_column_headers = ['country', 'homeland', 'state', 'nation', 'kingdom']
city_sensitive_column_headers = ['city', 'town' 'capital', 'metropolis', 'downtown', 'village', 'megalopolis']
municipality_sensitive_column_headers = ['municipality', 'community', 'district', 'borough', 'township', 'precinct']
postal_codes_sensitive_column_headers = ['zip_code', 'zip', 'postal', 'post', 'postal_code', 'post_code']
state_sensitive_column_headers = ['state']


def lexeme_search(token: str, searchable: list):
    tokens = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>? ]', token)
    mask = map(lambda x: True if str(x).lower() in searchable else False, tokens)
    return any(mask)


def latitude_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x,  latitude_sensitive_column_headers) else 0, data_frame.columns)
    return score


def longitude_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, longitude_sensitive_column_headers) else 0, data_frame.columns)
    return score


def country_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, country_sensitive_column_headers) else 0, data_frame.columns)
    return score


def city_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, city_sensitive_column_headers) else 0, data_frame.columns)
    return score


def municipality_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, municipality_sensitive_column_headers) else 0, data_frame.columns)
    return score


def state_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, state_sensitive_column_headers) else 0, data_frame.columns)
    return score


def latitude_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    regex_latitude = '^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$'

    # search for latitude
    r = re.compile(regex_latitude)
    for column in columns:
        if data_frame[column].dtype == 'float64' or data_frame[column].dtype == 'float32':
            decimal_part = data_frame[column].fillna(0.0).astype('int')
            if max(decimal_part) <= 90 and min(decimal_part) >= -90:
                mask = data_frame[column].apply(lambda x: bool(r.match(str(x))))
                total = mask.sum()
                score = (total / len(data_frame)) * 100
                statistic_match.append(score)
            else:
                statistic_match.append(0.0)
        else:
            statistic_match.append(0.0)

    return statistic_match


def longitude_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    regex_longitude = '^\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'

    # search for longitude
    r = re.compile(regex_longitude)
    for column in columns:
        if data_frame[column].dtype == 'float64' or data_frame[column].dtype == 'float32':
            decimal_part = data_frame[column].fillna(0.0).astype('int')
            if max(decimal_part) <= 180 and min(decimal_part) >= -180:
                mask = data_frame[column].apply(lambda x: bool(r.match(str(x))))
                total = mask.sum()
                score = (total / len(data_frame)) * 100
                statistic_match.append(score)
            else:
                statistic_match.append(0.0)
        else:
            statistic_match.append(0.0)

    return statistic_match


def country_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/location/airport.csv', usecols=['country'])
    df['country'] = df['country'].apply(lambda x: str(x).lower())
    df.drop_duplicates(subset=['country'], inplace=True)
    df.replace('nan', np.nan, inplace=True)
    df.dropna(inplace=True)

    statistic_match = []
    for column in columns:
        if data_frame[column].dtype == 'object':
            data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
            mask = pd.Series(data_frame[column]).isin(pd.Series(df['country']))
            total = sum(mask)
            factor = total / len(data_frame[column])
            score = factor * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def city_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/location/airport.csv', usecols=['city'])
    df['city'] = df['city'].apply(lambda x: str(x).lower())
    df.drop_duplicates(subset=['city'], inplace=True)
    df.replace('nan', np.nan, inplace=True)
    df.dropna(inplace=True)

    statistic_match = []

    for column in columns:
        if data_frame[column].dtype == 'object':
            data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
            mask = pd.Series(data_frame[column]).isin(pd.Series(df['city']))
            total = sum(mask)
            factor = total / len(data_frame)
            score = factor*100

            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def municipality_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/location/airport.csv', usecols=['municipality'])
    df['municipality'] = df['municipality'].apply(lambda x: str(x).lower())
    df.drop_duplicates(subset=['municipality'], inplace=True)
    df.replace('nan', np.nan, inplace=True)
    df.dropna(inplace=True)

    statistic_match = []

    for column in columns:
        if data_frame[column].dtype == 'object':
            data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
            mask = pd.Series(data_frame[column]).isin(pd.Series(df['municipality']))
            total = sum(mask)
            factor = total / len(data_frame)

            score = factor * 100

            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def state_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/location/airport.csv', usecols=['state'])
    df['state'] = df['state'].apply(lambda x: str(x).lower())
    df.drop_duplicates(subset=['state'], inplace=True)
    df.replace('nan', np.nan, inplace=True)
    df.dropna(inplace=True)

    statistic_match = []

    for column in columns:
        if data_frame[column].dtype == 'object':
            data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
            mask = pd.Series(data_frame[column]).isin(pd.Series(df['state']))
            total = sum(mask)
            factor = total / len(data_frame)

            score = factor * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def search(data_frame, pii_scale):
    result = []

    # Latitude
    latitude_scores = list(map(pii_scale, latitude_search_on_column_basis(data_frame), latitude_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(latitude_scores[i], 1), 'match': 'Latitude', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if latitude_scores[i] > 10.0]

    # Longitude
    longitude_scores = list(map(pii_scale, longitude_search_on_column_basis(data_frame), longitude_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(longitude_scores[i], 1), 'match': 'Longitude', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if longitude_scores[i] > 10.0]

    # Country
    country_scores = list(map(pii_scale, country_search_on_column_basis(data_frame), country_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(country_scores[i], 1), 'match': 'Country', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if country_scores[i] > 10.0]

    # City
    city_scores = list(map(pii_scale, city_search_on_column_basis(data_frame), city_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(city_scores[i], 1),  'match': 'City', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if city_scores[i] > 10.0]

    # Municipality
    municipality_scores = list(map(pii_scale, municipality_search_on_column_basis(data_frame), municipality_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(municipality_scores[i], 1), 'match': 'Municipality', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if municipality_scores[i] > 10.0]

    # State
    state_scores = list(map(pii_scale, state_search_on_column_basis(data_frame), state_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(state_scores[i], 1), 'match': 'State', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if state_scores[i] > 10.0]

    return result
