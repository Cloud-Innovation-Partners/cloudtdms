#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import socket
import re

ip_sensitive_column_headers = ['ipaddress', 'ip', 'ipadd', 'InternetProtocoladdress']

mac_sensitive_column_headers = ['mac']
msisdn_sensitive_column_headers = ['imeis', 'msisdn']
imsi_sensitive_column_headers = ['imsi']
guid_sensitive_column_headers = ['guid']
hardware_serial_sensitive_column_headers = ['serial', 'hardware']


def lexeme_search(token: str, searchable: list):
    tokens = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>? ]', token)
    mask = map(lambda x: True if str(x).lower() in searchable else False, tokens)
    return any(mask)


def ip_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, ip_sensitive_column_headers) else 0, data_frame.columns)
    return score


def valid_ip(address):
    regex_ip = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    pattern = re.compile(regex_ip)
    return True if pattern.search(address) else False


def ip_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        if data_frame[column].dtype == 'object':
            mask = data_frame[column].apply(valid_ip)
            total = mask.sum()
            score = (total / len(data_frame)) * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def mac_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, mac_sensitive_column_headers) else 0, data_frame.columns)
    return score


def _is_valid_mac(mac):
    regex_mac = "^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$"
    mac = str(mac).lower()
    pattern = re.compile(regex_mac)
    return True if pattern.search(mac) else False


def mac_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        if data_frame[column].dtype == 'object':
            mask = data_frame[column].apply(_is_valid_mac)
            total = mask.sum()
            score = (total / len(data_frame)) * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def msisdn_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, msisdn_sensitive_column_headers) else 0, data_frame.columns)
    return score


def msisdn_search_on_data_basis(data_frame):
    return [0.0]* len(data_frame.columns)


def imsi_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, imsi_sensitive_column_headers) else 0, data_frame.columns)
    return score


def imsi_search_on_data_basis(data_frame):
    return [0.0]*len(data_frame.columns)


def guid_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, guid_sensitive_column_headers) else 0, data_frame.columns)
    return score


def _is_valid_guid(guid):
    guid = str(guid).lower()
    regex_guid = "^{?[0-9a-f]{8}-?[0-9a-f]{4}-?[1-5][0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}}?$"
    pattern = re.compile(regex_guid)
    return True if pattern.search(guid) else False


def guid_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        if data_frame[column].dtype == 'object':
            mask = data_frame[column].apply(_is_valid_guid)
            total = mask.sum()
            score = (total / len(data_frame)) * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)
    return statistic_match


def hardware_serial_search_on_column_basis(data_frame):
    score = map(lambda x: 50 if lexeme_search(x, hardware_serial_sensitive_column_headers) else 0, data_frame.columns)
    return score


def _is_valid_sn(sn):
    sn = str(sn).lower()
    regex_sn = "^([0-9a-z]|[0-9]){8,12}$"
    pattern = re.compile(regex_sn)
    return True if pattern.search(sn) else False


def hardware_serial_search_on_data_basis(data_frame):
    columns = data_frame.columns

    # Load Sample Data
    statistic_match = []
    for column in columns:
        if data_frame[column].dtype == 'object':
            mask = data_frame[column].apply(_is_valid_sn)
            total = mask.sum()
            score = (total / len(data_frame)) * 100
            statistic_match.append(score)
        else:
            statistic_match.append(0.0)

    return statistic_match


def search(data_frame, pii_scale):
    result = []

    # IP
    ip_scores = list(map(pii_scale, ip_search_on_column_basis(data_frame), ip_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(ip_scores[i], 1), 'match': 'IP', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if ip_scores[i] > 10.0]

    # GUID
    guid_scores = list(map(pii_scale, guid_search_on_column_basis(data_frame), guid_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(guid_scores[i], 1), 'match': 'GUID', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if guid_scores[i] > 10.0]

    # MAC
    mac_scores = list(map(pii_scale, mac_search_on_column_basis(data_frame), mac_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(mac_scores[i], 1), 'match': 'MAC', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if mac_scores[i] > 10.0]

    # # HardwareSerial
    # hardware_serial_scores = list(map(pii_scale, hardware_serial_search_on_column_basis(data_frame), hardware_serial_search_on_data_basis(data_frame)))
    # result += [{data_frame.columns[i]: round(hardware_serial_scores[i], 1), 'match': 'Hardware_Serial', 'sensitivity': 'high', 'basis': 'pii_scale'}
    #            for i in range(len(data_frame.columns)) if hardware_serial_scores[i] > 10.0]

    # MSISDN
    msisdn_serial_scores = list(map(pii_scale, msisdn_search_on_column_basis(data_frame), msisdn_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(msisdn_serial_scores[i], 1), 'match': 'MSISDN', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if msisdn_serial_scores[i] > 10.0]

    # IMSI
    imsi_serial_scores = list(map(pii_scale, imsi_search_on_column_basis(data_frame), imsi_search_on_data_basis(data_frame)))
    result += [{data_frame.columns[i]: round(imsi_serial_scores[i], 1), 'match': 'IMSI', 'sensitivity': 'high', 'basis': 'pii_scale'}
               for i in range(len(data_frame.columns)) if imsi_serial_scores[i] > 10.0]

    return result
