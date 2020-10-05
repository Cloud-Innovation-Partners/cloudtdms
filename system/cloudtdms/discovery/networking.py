#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import socket
import re

ip_sensitive_column_headers = ['ipaddress', 'ip address', 'ip_address', 'ipadd', 'ip add', 'ip_add',
                               'Internet Protocol address',
                               'Internet_Protocol_address', 'host identity', 'host_identity', 'IP number', 'IP_number',
                               'network identity', 'network_identity', 'network identification',
                               'network_identification',
                               ]

mac_sensitive_column_headers = ['mac', 'mac address', 'mac_address', 'mac_add']
msisdn_sensitive_column_headers = ['imeis', 'msidn', 'iccids', 'tmsis', 'msidsn', 'msidsns', 'esns', 'msin', 'misdn',
                                   'MSISDN']
imsi_sensitive_column_headers = ['imsi', 'IMSI', 'International Mobile Subscriber Identity',
                                 'International_Mobile_Subscriber_Identity',
                                 'international mobile subscriber identity',
                                 'international_mobile_subscriber_identity']
guid_sensitive_column_headers = ['guid', 'GUID', 'Globally_Unique_Identifier', 'Globally Unique Identifier',
                                 'GloballyUniqueIdentifier', 'globally_unique_identifier', 'globally unique identifier']
hardware_serial_sensitive_column_headers = ['Serial Number', 'Serial_Number', 'serial_number', 'serial number',
                                            'hardware_serial_number', 'hardware serial number',
                                            'Hardware_Serial_Number', 'Hardware Serial Number']


def ip_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'IP', 'sensitvity': 'high', 'basis': 'column_name'} for f in column_headers if
                       f in ip_sensitive_column_headers]
    return matched_columns


def valid_ip(address):
    regex_ip = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    pattern = re.compile(regex_ip)
    return True if pattern.search(address) else False


def ip_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        pass

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        mask = data_frame[column].apply(valid_ip)
        total = mask.sum()
        score = (total / len(data_frame)) * 100
        if score >= 50:
            statistic_match.append({column: int(score), 'match': 'IP', 'sensitvity': 'high', 'basis': 'column_data'})
    return statistic_match


def mac_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'MAC', 'sensitvity': 'high', 'basis': 'column_name'} for f in column_headers if
                       f in mac_sensitive_column_headers]
    return matched_columns


def _is_valid_mac(mac):
    regex_mac = "^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$"
    mac = str(mac).lower()
    pattern = re.compile(regex_mac)
    return True if pattern.search(mac) else False


def mac_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        mask = data_frame[column].apply(_is_valid_mac)
        total = mask.sum()
        score = (total / len(data_frame)) * 100
        if score >= 50:
            statistic_match.append({column: int(score), 'match': 'MAC', 'sensitvity': 'high', 'basis': 'column_data'})
    return statistic_match


def msisdn_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'MSISDN', 'sensitvity': 'high', 'basis': 'column_name'} for f in column_headers
                       if f in msisdn_sensitive_column_headers]
    return matched_columns


def imsi_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'IMSI', 'sensitvity': 'high', 'basis': 'column_name'} for f in column_headers if
                       f in imsi_sensitive_column_headers]
    return matched_columns


def guid_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'GUID', 'sensitvity': 'high', 'basis': 'column_name'} for f in column_headers if
                       f in guid_sensitive_column_headers]
    return matched_columns


def _is_valid_guid(guid):
    guid = str(guid).lower()
    regex_guid = "^{?[0-9a-f]{8}-?[0-9a-f]{4}-?[1-5][0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}}?$"
    pattern = re.compile(regex_guid)
    return True if pattern.search(guid) else False


def guid_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        mask = data_frame[column].apply(_is_valid_guid)
        total = mask.sum()
        score = (total / len(data_frame)) * 100
        if score >= 50:
            statistic_match.append({column: int(score), 'match': 'GUID', 'sensitvity': 'high', 'basis': 'column_data'})
    return statistic_match


def hardware_serial_search_on_column_basis(data_frame, matched):
    column_headers = data_frame.columns
    matched_columns = [{f: 90, 'match': 'Hardware_Serial', 'sensitvity': 'high', 'basis': 'column_name'} for f in
                       column_headers if f in hardware_serial_sensitive_column_headers]
    return matched_columns


def _is_valid_sn(sn):
    sn = str(sn).lower()
    regex_sn = "^([0-9a-z]|[0-9]){8,12}$"
    pattern = re.compile(regex_sn)
    return True if pattern.search(sn) else False


def hardware_serial_search_on_data_basis(data_frame, matched):
    try:
        data_frame.drop(matched, inplace=True, axis=1)
    except KeyError:
        print("No columns available for drop operation!")

    data_frame = data_frame[data_frame.columns[(data_frame.applymap(type) == str).all(0)]]

    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        mask = data_frame[column].apply(_is_valid_sn)
        total = mask.sum()
        score = (total / len(data_frame)) * 100
        if score >= 50:
            statistic_match.append(
                {column: int(score), 'match': 'Hardware_Serial', 'sensitvity': 'high', 'basis': 'column_data'})
    return statistic_match


def search(data_frame):
    result = []
    result = ip_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += guid_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += hardware_serial_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += msisdn_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += imsi_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += mac_search_on_column_basis(data_frame, [list(f.items())[0][0] for f in result])

    result += ip_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += mac_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += guid_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])
    result += hardware_serial_search_on_data_basis(data_frame, [list(f.items())[0][0] for f in result])

    # return list(set(result))

    return result
