#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

# Contains Search Rules for Identifying Person Details in User Data

import pandas as pd
import re

age_sensitive_column_headers = ['age', 'maturity', 'seniority', 'years', 'duration', 'age_group', 'oldness']
gender_sensitive_column_headers = ['gender', 'sex', 'kind', 'sexuality', 'male', 'female', 'identity', 'neuter']
email_sensitive_column_headers = ['email', 'mail', 'e-mail', 'message', 'electronic_mail', 'post', 'correspondence',
                                  'send', 'mailing', 'memo', 'mailbox', 'write']
dob_sensitive_column_headers = ['dob', 'date_of_birth', 'birth_date', 'birth date', 'date of birth', 'D.O.B', 'DOB']
credit_card_sensitive_column_headers = ['credit_card_num', 'credit_card_number', 'credit_card', 'credit card']
ssn_sensitive_column_headers = ['ssn', 'social_security_number', 'social security number', 'National ID number',
                                'National_ID_number', ' national id number', 'national_id_number']
blood_group_sensitive_column_headers = ['bg', 'blood group', 'blood_group', 'blood Group', 'Blood_Group']


def age_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if x in age_sensitive_column_headers else 0, data_frame.columns)
    return score


def gender_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if x in gender_sensitive_column_headers else 0, data_frame.columns)
    return score


def email_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if x in email_sensitive_column_headers else 0, data_frame.columns)
    return score


def dob_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if x in dob_sensitive_column_headers else 0, data_frame.columns)
    return score


def cc_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if x in credit_card_sensitive_column_headers else 0, data_frame.columns)
    return score


def ssn_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if x in ssn_sensitive_column_headers else 0, data_frame.columns)
    return score


def blood_group_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if x in blood_group_sensitive_column_headers else 0, data_frame.columns)
    return score


def gender_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    df_1 = pd.DataFrame({'gender': ['male', 'female']})
    df_2 = pd.DataFrame({'gender': ['m', 'f']})

    statistic_match = []

    for column in columns:
        if data_frame.columns.dtype == 'object':
            df = pd.DataFrame(data_frame[column].drop_duplicates())
            df[column] = df[column].apply(lambda x: str(x).lower())
            mask1 = pd.Series(df[column]).isin(pd.Series(df_1['gender']))
            mask2 = pd.Series(df[column]).isin(pd.Series(df_2['gender']))

            sum1 = mask1.sum()
            sum2 = mask2.sum()
            total = max(sum1, sum2)
            factor = total/len(df)
            score = factor*100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def age_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    df = pd.DataFrame({'age': range(18, 81)})
    statistic_match = []

    for column in columns:
        if data_frame[column].dtype == 'int64' or data_frame[column].dtype == 'int32':
            if not max(data_frame[column]) > 100 and min(data_frame[column]) != 0:
                if not sorted(data_frame[column]) == list(range(min(data_frame[column]), max(data_frame[column]) + 1)):
                    mask = data_frame[column].isin(df['age'])
                    total = sum(mask)
                    factor = total / len(data_frame)
                score = factor * 100
                statistic_match.append(score)
            else:
                statistic_match.append(0.0)
        else:
            statistic_match.append(0.0)

    return statistic_match


def email_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    r = re.compile(regex)
    for column in columns:
        if data_frame[column].dtype == 'str':
            mask = data_frame[column].apply(lambda x: bool(r.match(x)))
            total = mask.sum()

            score = (total / len(data_frame)) * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def dob_search_on_data_basis(data_frame):
    columns = data_frame.columns

    regex_dob = "^\d{,2}[-/.]\d{,2}[-/.](17|18|19|20)\\d\\d|(17|18|19|20)\\d\\d[-/.]\d{,2}[-/.]\d{,2}$"
    pattern = re.compile(regex_dob)

    statistic_match = []

    for column in columns:
        if data_frame[column].dtype == 'object' or data_frame[column].dtype == 'datetime64[ns]':

            mask = data_frame[column].apply(lambda x: True if pattern.search(str(x)) else False)
            total = mask.sum()
            score = (total / len(data_frame)) * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def _is_valid_cc(cc):
    new_cc = ''
    for i in str(cc):
        if i.isdigit():
            new_cc += i
    regex_dob = "^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$"
    pattern = re.compile(regex_dob)
    return True if pattern.search(new_cc) else False


def cc_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        if data_frame[column].dtype == 'object':
            mask = data_frame[column].apply(_is_valid_cc)
            total = mask.sum()
            score = (total / len(data_frame)) * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def ssn_search_on_data_basis(data_frame):
    columns = data_frame.columns

    regex_ssn = "^(?!666|000|9\\d{2})\\d{3}(-)?(?!00)\\d{2}(-)?(?!0{4})\\d{4}$"
    pattern = re.compile(regex_ssn)

    # Load Sample Data
    statistic_match = []
    for column in columns:
        if data_frame[column].dtype == 'object':
            mask = data_frame[column].apply(lambda x: True if pattern.search(str(x)) else False)
            total = mask.sum()
            score = (total / len(data_frame)) * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def blood_group_search_on_data_basis(data_frame):
    columns = data_frame.columns

    regex_bg = "^(A|B|AB|O)[+-]$"
    pattern = re.compile(regex_bg)

    statistic_match = []
    for column in columns:
        if data_frame[column].dtype == 'object':
            mask = data_frame[column].apply(lambda x: True if pattern.search(str(x)) else False)
            total = mask.sum()
            score = (total / len(data_frame)) * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def search(data_frame, pii_scale: callable):
    result = []

    # Age
    age_scores = list(map(pii_scale, age_search_on_column_basis(data_frame), age_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(age_scores[i], 1), 'match': 'Age', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if age_scores[i] > 10.0]
    # Gender
    gender_scores = list(map(pii_scale, gender_search_on_column_basis(data_frame), gender_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(gender_scores[i], 1), 'match': 'Gender', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if gender_scores[i] > 10.0]

    # Email
    email_scores = list(map(pii_scale, email_search_on_column_basis(data_frame), email_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(email_scores[i], 1),  'match': 'Email', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if email_scores[i] > 10.0]

    # DOB
    dob_scores = list(map(pii_scale, dob_search_on_column_basis(data_frame), dob_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(dob_scores[i], 1), 'match': 'Date Of Birth', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if dob_scores[i] > 10.0]

    # Credit Card
    credit_card_scores = list(map(pii_scale, cc_search_on_column_basis(data_frame), cc_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(credit_card_scores[i], 1), 'match': 'Credit Card', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if credit_card_scores[i] > 10.0]

    # SocialSecurity
    social_security_scores = list(map(pii_scale, ssn_search_on_column_basis(data_frame), ssn_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(social_security_scores[i], 1), 'match': 'Social Security Number', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if social_security_scores[i] > 10.0]

    # BloodGroup
    blood_group_scores = list(map(pii_scale, blood_group_search_on_column_basis(data_frame), blood_group_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(blood_group_scores[i], 1), 'match': 'Social Security Number', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if blood_group_scores[i] > 10.0]

    return result
