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
dob_sensitive_column_headers = ['dob','date_of_birth','birth_date','birth date','date of birth','D.O.B','DOB']
credit_card_sensitive_column_headers = ['credt_card_num','credit_card_number','credit_card','credit card']
ssn_sensitive_column_headers = ['ssn','social_security_number','social security number','National ID number',
                                'National_ID_number',' national id number','national_id_number']
blood_group_sensitive_column_headers = ['bg','blood group','blood_group','blood Group','Blood_Group']


def age_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90,  'match': 'Age', 'sensitvity': 'high', 'basis' : 'column_name'} for f in column_headers if f in age_sensitive_column_headers]
    return matched_columns


def gender_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90,  'match': 'Gender', 'sensitvity': 'high', 'basis' : 'column_name'} for f in column_headers if f in gender_sensitive_column_headers]
    return matched_columns


def email_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90,  'match': 'Email','sensitvity': 'high', 'basis' : 'column_name'} for f in column_headers if f in email_sensitive_column_headers]
    return matched_columns

def dob_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'Date of Birth', 'sensitvity': 'high', 'basis' : 'column_name'} for f in column_headers if f in dob_sensitive_column_headers]
    return matched_columns

def cc_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'Credit Card', 'sensitvity': 'high', 'basis' : 'column_name'} for f in column_headers if f in credit_card_sensitive_column_headers]
    return matched_columns

def ssn_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'Social Security Number', 'sensitvity': 'high', 'basis' : 'column_name'} for f in column_headers if f in ssn_sensitive_column_headers]
    return matched_columns

def blood_group_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'Blood Group', 'sensitvity': 'high', 'basis' : 'column_name'} for f in column_headers if f in blood_group_sensitive_column_headers]
    return matched_columns

def gender_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        pass


    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    df_1 = pd.DataFrame({'gender':['male', 'female']})
    df_2 = pd.DataFrame({'gender':['m','f']})

    statistic_match = []

    for column in columns:

        df = pd.DataFrame(data_frame[column].drop_duplicates())
        df[column] = df[column].apply(lambda x: str(x).lower())
        mask1 = pd.Series(df[column]).isin(pd.Series(df_1['gender']))
        mask2 = pd.Series(df[column]).isin(pd.Series(df_2['gender']))

        sum1 = mask1.sum()
        sum2 = mask2.sum()
        score = max(sum1,sum2)/len(df)*100
        if score > 5:
            statistic_match.append({column: int(score), 'match': 'Gender', 'basis' : 'column_data'})
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
            score = (len(age_intersection) / len(df)) * 100
            if score > 5:
                statistic_match.append({column: int(score), 'match': 'Age', 'sensitvity': 'high', 'basis' : 'column_data'})
    return statistic_match


def email_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        pass

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    r = re.compile(regex)
    for column in columns:
        mask = data_frame[column].apply(lambda x: bool(r.match(x)))
        sum = mask.sum()
        if sum > 100:
            score = (sum / len(data_frame)) * 100
            if score > 5:
                statistic_match.append({column: int(score), 'match': 'Email', 'sensitvity': 'high', 'basis' : 'column_data'})
    return statistic_match

def _is_valid_dob(dob):
    regex_dob="^\d{,2}[-/.]\d{,2}[-/.](17|18|19|20)\\d\\d$"
    pattern = re.compile(regex_dob)
    return True if pattern.search(dob) else False

def dob_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        pass

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        mask = data_frame[column].apply(_is_valid_dob)
        sum = mask.sum()
        if sum > 100:
            score = (sum / len(data_frame)) * 100
            if score > 5:
                statistic_match.append({column: int(score), 'match': 'Date Of Birth','sensitvity': 'high', 'basis' : 'column_data'})

    return statistic_match

def _is_valid_cc(cc):
    new_cc=''
    for i in cc:
        if i.isdigit():
            new_cc+=i
    regex_dob="^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$"
    pattern = re.compile(regex_dob)
    return True if pattern.search(new_cc) else False


def cc_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        pass

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        mask = data_frame[column].apply(_is_valid_cc)
        sum = mask.sum()
        if sum > 100:
            score = (sum / len(data_frame)) * 100
            if score > 5:
                statistic_match.append({column: int(score), 'match': 'Credit Card', 'sensitvity': 'high', 'basis' : 'column_data'})

    return statistic_match

def _is_valid_ssn(ssn):
    regex_ssn = "^(?!666|000|9\\d{2})\\d{3}(-)?(?!00)\\d{2}(-)?(?!0{4})\\d{4}$"
    pattern = re.compile(regex_ssn)
    return True if pattern.search(ssn) else False

def ssn_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        pass

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        mask = data_frame[column].apply(_is_valid_ssn)
        sum = mask.sum()
        if sum > 100:
            score = (sum / len(data_frame)) * 100
            if score > 5:
                statistic_match.append({column:score, 'match': 'Social Security Number', 'sensitvity': 'high', 'basis' : 'column_data'})
    return statistic_match

def _is_valid_blood_group(blood_group):
    regex_bg = "^(A|B|AB|O)[+-]$"
    pattern = re.compile(regex_bg)
    return True if pattern.search(blood_group) else False

def blood_group_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        pass

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        mask = data_frame[column].apply(_is_valid_blood_group)
        sum = mask.sum()
        if sum > 100:
            score = (sum / len(data_frame)) * 100
            if score > 5:
                statistic_match.append({column: int(score), 'match': 'Blood Group','sensitvity': 'high',  'basis' : 'column_data'})
    return statistic_match

def search(data_frame):
    result = []
    result += age_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += gender_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += email_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += dob_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += cc_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += ssn_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += age_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += email_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += gender_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += dob_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += cc_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += ssn_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])

    return result