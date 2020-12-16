#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import re

phone_sensitive_column_headers = ['phone', 'contact', 'telephone', 'cell']


def lexeme_search(token: str, searchable: list):
    tokens = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', token)
    mask = map(lambda x: True if str(x).lower() in searchable else False, tokens)
    return any(mask)


def phone_number_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, phone_sensitive_column_headers) else 0, data_frame.columns)
    return score


def _is_valid_phone_number(number):
    regex_phone_number = "^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
    pattern = re.compile(regex_phone_number)
    return True if pattern.match(number) else False


def phone_number_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        if data_frame[column].dtype == 'object':
            mask = data_frame[column].apply(_is_valid_phone_number)
            total = mask.sum()
            score = (total / len(data_frame)) * 100

            statistic_match.append(score)
        else:
            statistic_match.append(0.0)
    return statistic_match


def search(data_frame, pii_scale):
    result = []

    # PhoneNumber
    phone_number_scores = list(map(pii_scale, phone_number_search_on_column_basis(data_frame), phone_number_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(phone_number_scores[i], 1), 'match': 'Phone_Number', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if phone_number_scores[i] > 10.0]

    return result
