#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import numpy as np
import pandas as pd
from functools import reduce
from system.dags import get_providers_home
import re


coord_sensitive_column_headers = ['latitude', 'longitude','lat','long','altitude','azimuth','ordinate','abscissa',
                            'right ascension','declension']
country_sensitive_column_headers=['country','homeland','native land','native_land','grass roots','grass_roots','land']
city_sensitive_column_headers=['city','capital','center','metropolis','downtown','place','port','polis','urbs']
municipality_sensitive_column_headers=['municipality','community','district','town','township','village'
                                      ,'borough','precinc']
postal_codes_sensitive_column_headers=['zip','pincode','pin_code','pin code','postalcode', 'postal_code','postal code']
state_sensitive_column_headers=['state']

def coord_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [f for f in column_headers if f in coord_sensitive_column_headers]
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
    regex_longitude='^\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'

    #search for latitude
    r = re.compile(regex_latitude)
    for column in columns:
        mask = data_frame[column].apply(lambda x: bool(r.match(str(x))))
        if mask.sum() > 100:
            statistic_match.append(column)

    # search for longitude
    r = re.compile(regex_longitude)
    for column in columns:
        mask = data_frame[column].apply(lambda x: bool(r.match(str(x))))
        if mask.sum() > 100:
            statistic_match.append(column)
            
    statistic_match = list(set(statistic_match))

    return statistic_match

def country_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [f for f in column_headers if f in country_sensitive_column_headers]
    return matched_columns

def country_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/location/airport.csv',usecols=['country'])
    df['country'] = df['country'].apply(lambda x: str(x).lower())
    df.drop_duplicates(subset=['country'], inplace=True)
    statistic_match = []

    for column in columns:
        data_frame[column]=data_frame[column].apply(lambda x:str(x).lower())
        country_intersection = reduce(np.intersect1d, [data_frame[column], df['country']])
        if len(country_intersection) >=3:
            statistic_match.append(column)

    return statistic_match

def city_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [f for f in column_headers if f in city_sensitive_column_headers]
    return matched_columns

def city_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    df = pd.read_csv(f'{get_providers_home()}/location/airport.csv',usecols=['city'])
    df['city'] = df['city'].apply(lambda x: str(x).lower())
    df.drop_duplicates(subset=['city'], inplace=True)
    statistic_match = []

    for column in columns:
        data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
        city_intersection = reduce(np.intersect1d, [data_frame[column], df['city']])
        if len(city_intersection) > 100:
            statistic_match.append(column)

    return statistic_match


def municipality_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [f for f in column_headers if f in municipality_sensitive_column_headers]
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
        data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
        city_intersection = reduce(np.intersect1d, [data_frame[column], df['municipality']])
        if len(city_intersection) > 100:
            statistic_match.append(column)

    return statistic_match

def state_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [f for f in column_headers if f in state_sensitive_column_headers]
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
        data_frame[column] = data_frame[column].apply(lambda x: str(x).lower())
        city_intersection = reduce(np.intersect1d, [data_frame[column], df['state']])
        if len(city_intersection) > 100:
            statistic_match.append(column)

    return statistic_match

def search(data_frame):
    result = []
    result = coord_search_on_column_basis(data_frame,result)
    result += coord_search_on_data_basis(data_frame, result)
    result += country_search_on_column_basis(data_frame,result)
    result += country_search_on_data_basis(data_frame, result)
    result += city_search_on_column_basis(data_frame, result)
    result += city_search_on_data_basis(data_frame, result)
    result += municipality_search_on_column_basis(data_frame, result)
    result += municipality_search_on_data_basis(data_frame, result)
    result += state_search_on_column_basis(data_frame, result)
    result += state_search_on_data_basis(data_frame, result)

    return list(set(result))