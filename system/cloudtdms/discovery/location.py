#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import numpy as np
import pandas as pd
from functools import reduce
from system.dags import get_providers_home
import re

latitude_sensitive_column_headers = ['latitude', 'lat', 'altitude']
longitude_sensitive_column_headers = ['longitude', 'long']
country_sensitive_column_headers = ['country', 'homeland', 'native land', 'native_land', 'grass roots', 'grass_roots',
                                    'land']
city_sensitive_column_headers = ['city', 'capital', 'center', 'metropolis', 'downtown', 'place', 'port', 'polis',
                                 'urbs']
municipality_sensitive_column_headers = ['municipality', 'community', 'district', 'town', 'township', 'village'
    , 'borough', 'precinct']
postal_codes_sensitive_column_headers = ['zip', 'pincode', 'pin_code', 'pin code', 'postalcode', 'postal_code',
                                         'postal code', 'post']
state_sensitive_column_headers = ['state']


def latitude_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'Latitude', 'sensitvity': 'high', 'basis': 'column_name'} for f in
                       column_headers if f in latitude_sensitive_column_headers]
    return matched_columns


def longitude_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'Longitude', 'sensitvity': 'high', 'basis': 'column_name'} for f in
                       column_headers if f in longitude_sensitive_column_headers]
    return matched_columns


def coord_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == float).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    regex_latitude = '^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$'
    regex_longitude = '^\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'

    matched_latitudes = []

    # search for latitude
    r = re.compile(regex_latitude)
    for column in columns:
        if data_frame[column].dtype == 'float64' or data_frame[column].dtype == 'float32':
            decimal_part = data_frame[column].fillna(0.0).astype('int')
            if max(decimal_part) <= 90 and min(decimal_part) >= -90:
                mask = data_frame[column].apply(lambda x: bool(r.match(str(x))))
                total = mask.sum()
                score = (total / len(data_frame)) * 100
                if score >= 50:
                    statistic_match.append(
                        {column: int(score), 'match': 'Latitude', 'sensitvity': 'high', 'basis': 'column_data'})
                    matched_latitudes.append(column)

    # search for longitude
    r = re.compile(regex_longitude)
    for column in columns:
        if column not in matched_latitudes:
            if data_frame[column].dtype == 'float64' or data_frame[column].dtype == 'float32':
                decimal_part = data_frame[column].fillna(0.0).astype('int')
                if max(decimal_part) <= 180 and min(decimal_part) >= -180:
                    mask = data_frame[column].apply(lambda x: bool(r.match(str(x))))
                    total = mask.sum()
                    score = (total / len(data_frame)) * 100
                    if score >= 50:
                        statistic_match.append(
                            {column: int(score), 'match': 'Longitude', 'sensitvity': 'high', 'basis': 'column_data'})

    # statistic_match = list(set(statistic_match))

    return statistic_match


def country_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'Country', 'sensitvity': 'high', 'basis': 'column_name'} for f in column_headers
                       if f in country_sensitive_column_headers]
    return matched_columns


def country_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/location/airport.csv', usecols=['country'])
    df['country'] = df['country'].apply(lambda x: str(x).lower())
    df.drop_duplicates(subset=['country'], inplace=True)
    statistic_match = []
    for column in columns:
        if data_frame[column].dtype == 'object':
            data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
            mask = pd.Series(data_frame[column]).isin(pd.Series(df['country']))
            total = sum(mask)
            factor = total / len(data_frame[column])
            score = factor * 100
            if score >= 50:
                statistic_match.append(
                    {column: int(score), 'match': 'Country', 'sensitvity': 'high', 'basis': 'column_data'})

    return statistic_match


def city_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'City', 'sensitvity': 'high', 'basis': 'column_name'} for f in column_headers if
                       f in city_sensitive_column_headers]
    return matched_columns


def city_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/location/airport.csv', usecols=['city'])
    df['city'] = df['city'].apply(lambda x: str(x).lower())
    df.drop_duplicates(subset=['city'], inplace=True)
    statistic_match = []

    for column in columns:
        if data_frame[column].dtype == 'object':
            data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
            mask = pd.Series(data_frame[column]).isin(pd.Series(df['city']))
            total = sum(mask)
            factor = total / len(data_frame)
            score = factor*100
            if score >= 50:
                statistic_match.append(
                    {column: int(score), 'match': 'City', 'sensitvity': 'high', 'basis': 'column_data'})

    return statistic_match


def municipality_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'Municipality', 'sensitvity': 'high', 'basis': 'column_name'} for f in
                       column_headers if f in municipality_sensitive_column_headers]
    return matched_columns


def municipality_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/location/airport.csv', usecols=['municipality'])
    df['municipality'] = df['municipality'].apply(lambda x: str(x).lower())
    df.drop_duplicates(subset=['municipality'], inplace=True)
    statistic_match = []

    for column in columns:
        if data_frame[column].dtype == 'object':
            data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
            mask = pd.Series(data_frame[column]).isin(pd.Series(df['municipality']))
            total = sum(mask)
            factor = total / len(data_frame)

            score = factor * 100
            if score >= 50:
                statistic_match.append(
                    {column: int(score), 'match': 'Municipality', 'sensitvity': 'high', 'basis': 'column_data'})
    return statistic_match


def state_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'State', 'sensitvity': 'high', 'basis': 'column_name'} for f in column_headers
                       if f in state_sensitive_column_headers]
    return matched_columns


def state_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/location/airport.csv', usecols=['state'])
    df['state'] = df['state'].apply(lambda x: str(x).lower())
    df.drop_duplicates(subset=['state'], inplace=True)
    statistic_match = []

    for column in columns:
        if data_frame[column].dtype == 'object':
            data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
            mask = pd.Series(data_frame[column]).isin(pd.Series(df['state']))
            total = sum(mask)
            factor = total / len(data_frame)

            score = factor * 100
            if score >= 50:
                statistic_match.append(
                    {column: int(score), 'match': 'State', 'sensitvity': 'high', 'basis': 'column_data'})

    return statistic_match


def search(data_frame):
    result = []
    result += latitude_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += longitude_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += country_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += city_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += municipality_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += state_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])

    result += country_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += city_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += municipality_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += state_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += coord_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])

    # return list(set(result))
    return result
