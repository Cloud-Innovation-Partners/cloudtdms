#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import re

phone_sensitive_column_headers = ['phone_number', 'phone number', 'contact', 'contact_number','contact number','number']


def phone_number_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90.0, 'match': 'Phone_Number', 'sensitvity': 'high', 'basis' : 'column_name'}  for f in column_headers if f in phone_sensitive_column_headers]
    return matched_columns

def _is_valid_phone_number(number):
    regex_phone_number="^((\+)?([0-9]{,3}))?(-|\s)?(\()?[0-9]{3}(\))?(-|\s)?[0-9]{3}(-|\s)?[0-9]{4}$"
    pattern = re.compile(regex_phone_number)
    return True if pattern.match(number) else False

def phone_number_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        mask = data_frame[column].apply(_is_valid_phone_number)
        sum = mask.sum()
        if sum > 50:
            score = (sum / len(data_frame)) * 100
            statistic_match.append({column: score, 'match': 'Phone_Number', 'sensitvity': 'high', 'basis': 'column_data'})

    return statistic_match

def search(data_frame):
    result = []
    result = phone_number_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += phone_number_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    return result
