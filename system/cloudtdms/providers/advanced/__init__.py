#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import hashlib
import re
import os
import random
import pandas as pd
import numpy as np
import base64
import onetimepad
from Crypto.Cipher import AES
from airflow.utils.log.logging_mixin import LoggingMixin
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from airflow.configuration import get_airflow_home


def advanced(data_frame, number, args):
    field_names = {}
    for k in args:
        if k == 'locale':
            continue
        if k.split('-$-', 2)[1] not in field_names:
            field_names[k.split('-$-', 2)[1]] = {k.split('-$-', 2)[0]: args.get(k)}
        else:
            field_names[k.split('-$-', 2)[1]][k.split('-$-', 2)[0]] = args.get(k)

    columns = field_names.keys()

    for col in columns:
        mod = globals()[col]
        mod(data_frame, number, field_names.get(col))


# {'adv2': {'set_val': '1,2,3,4,5'}, 'adv4': {'set_val': '100,200,300,400,500'}}
# ['custom_list', 'custom_list1']
def custom_list(data_frame, number, args=None):
    """
    Generator function for custom_list
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("custom_list")]
    for column_name, data_frame_col_name in zip(args, dcols):
        set_val = args.get(column_name).get('set_val', "") if args is not None else ""
        data_frame[data_frame_col_name] = [random.choice(set_val.split(',')) for _ in range(int(number))]
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def set_null(data_frame, column):
    data_frame[column]=np.nan

def get_key(custom_key):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(custom_key)
    return base64.urlsafe_b64encode(digest.finalize())

def encryption(record, key):
    f = Fernet(get_key(bytes(key, 'utf-8')))
    encoded_text = f.encrypt(bytes(str(record), 'utf-8'))
    return encoded_text
    # decoded_text = cipher_suite.decrypt(encoded_text)


def caesar(record, key):
    result = ""
    key=int(key)
    # transverse the plain text
    for i in range(len(record)):
        char = record[i]
        # Encrypt uppercase characters in plain text

        if (char.isupper()):
            result += chr((ord(char) + key - 65) % 26 + 65)
        # Encrypt lowercase characters in plain text
        else:
            result += chr((ord(char) + key - 97) % 26 + 97)
    return result

def monoalpha_cipher(record):
    monoalpha_cipher_list = {'a': 'm', 'A': 'M', 'b': 'n', 'B': 'N', 'c': 'b', 'C': 'B', 'd': 'v', 'D': 'V', 'e': 'c', 'E': 'C', 'f': 'x', 'F': 'X', 'g': 'z', 'G': 'Z', 'h': 'a', 'H': 'A', 'i': 's', 'I': 'S', 'j': 'd', 'J': 'D', 'k': 'f', 'K': 'F', 'l': 'g', 'L': 'G', 'm': 'h', 'M': 'H', 'n': 'j', 'N': 'J', 'o': 'k', 'O': 'K', 'p': 'l', 'P': 'L', 'q': 'p', 'Q': 'P', 'r': 'o', 'R': 'O', 's': 'i', 'S': 'I', 't': 'u', 'T': 'U', 'u': 'y', 'U': 'Y', 'v': 't', 'V': 'T', 'w': 'r', 'W': 'R', 'x': 'e', 'X': 'E', 'y': 'w', 'Y': 'W', 'z': 'q', 'Z': 'Q', ' ': ' '}
    updated_record=''
    for i in record:
        updated_record+= monoalpha_cipher_list.get(i,i)
    return updated_record

def onetime(record, key):
    record =str(record)
    cipher = onetimepad.encrypt(record, key)
    return cipher

#AES
    # pad with spaces at the end of the text
    # beacuse AES needs 16 byte blocks
def pad(key):
    block_size = 16
    remainder = len(key) % block_size
    padding_needed = block_size - remainder
    return key + padding_needed * ' '

salt = b'J\x12\xeb0\xc0\x1c_\xee"\xdd\x95\x13\x17\xe5F\xe0'
iv = b'\x84S\\__\x83\x1fG,\x17\xc1W\xc7\xd0$\xb8'

def encrypt_aes(record, key):
    record=str(record)
    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(key.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    # pad text with spaces to be valid for AES CBC mode
    padded_record = pad(record)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_CBC, iv)

    # return a dictionary with the encrypted text
    return cipher_config.encrypt(padded_record)

def encrypt(data_frame, column, key, type):
    if type == 'fernet':
        data_frame[column]=data_frame[column].apply(encryption, key=key)
    elif type == 'caesar':
        data_frame[column] = data_frame[column].apply(caesar, key=key)
    elif type == 'monoaplha':
        data_frame[column] = data_frame[column].apply(monoalpha_cipher)
    elif type == 'onetimepad':
        data_frame[column] = data_frame[column].apply(onetime, key=key)
    elif type == 'aes':
        data_frame[column] = data_frame[column].apply(encrypt_aes, key=key)
    else:
        LoggingMixin().log.error("Invalid encryption type in attributes")

def masking(record, with_, character, from_):
    record = str(record)
    characters = int(character)
    if from_ == 'start':
        if len(record) < characters:
            record = with_ * len(record)
        else:
            record = with_ * characters + record[characters:]
    elif from_ == 'end':
        if len(record) < characters:
            record = with_ * len(record)
        else:
            record = record[:-characters] + with_ * characters
    elif from_ == 'mid':
        if len(record) < characters:
            record = with_ * len(record)
        else:
            record_length = len(record)
            remaining = record_length - int(characters)
            right = int(remaining / 2)
            sub_part = record[:right] + with_ * characters
            record = sub_part + record[len(sub_part):]
    else:
        LoggingMixin().log.error("Invalid masking attributes...")
    return record


def mask_out(data_frame, column, with_, character, from_):
    data_frame[column]=data_frame[column].apply(masking,with_=with_, character=character, from_=from_)


def shuffle(data_frame, column):
    data_frame[column]=data_frame[column].sample(frac=1).reset_index(drop=True)

def custom_file(data_frame, number, args=None):

    data_path = f"{os.path.dirname(get_airflow_home())}/user-data"
    dcols = [f for f in data_frame.columns if f.startswith("custom_file")]
    for column_name, data_frame_col_name in zip(args, dcols):
        ignore_headers = str(args.get(column_name).get('ignore_headers', 'yes')).lower()

        if ignore_headers not in ['no', 'yes']:
            ignore_headers = 'yes'

        name = args.get(column_name).get('name')
        column = args.get(column_name).get('column')

        if name is None:
            raise AttributeError(f"No value found for attribute `name` in `advanced.custom_file` schema entry!")
        if column is None:
            raise AttributeError(f"No value found for attribute `column` in `advanced.custom_file` schema entry!")
        if ignore_headers == 'yes' and not str(column).isdigit():
            raise AttributeError(f"Invalid value found for `column` attribute in `advanced.custom_file` schema entry, `column` cannot be string value when ignore_headers='yes' !")
        elif ignore_headers == 'no' and str(column).isdigit():
            raise AttributeError(f"Invalid value found for `column` attribute in `advanced.custom_file` schema entry, `column` cannot be int value when ignore_headers='no' !")

        file_path = f"{data_path}/{name}" if str(name).endswith('.csv') else f"{data_path}/{name}.csv"

        try:
            if not str(column).isdigit():
                df = pd.read_csv(file_path, usecols=[column])
                data_frame[data_frame_col_name] = [df[column].iloc[i%len(df)] for i in range(int(number))]
                data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)
            else:
                if int(column) < 0:
                    raise AttributeError(f"Invalid value found for `column` attribute in `advanced.custom_file` schema entry, `column` cannot have -ve int value as column index!")
                df = pd.read_csv(file_path, header=None, usecols=[int(column)], names=['custom_column'])
                data_frame[data_frame_col_name] = [df['custom_column'].iloc[i%len(df)] for i in range(int(number))]
                data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)
        except FileNotFoundError:
            raise

        if 'encrypt' in args.get(column):
            key=args.get(column).get('encrypt').get('key')
            type=args.get(column).get('encrypt').get('type','fernet').lower()
            encrypt(data_frame, column, key, type)
        elif 'shuffle' in args.get(column):
            shuffle_value=args.get(column).get('shuffle').lower()
            shuffle_value = True if shuffle_value == 'true' else False
            if shuffle_value:
                shuffle(data_frame, column)
        elif 'mask_out' in args.get(column):
            with_=args.get(column).get('mask_out').get('with')
            character=args.get(column).get('mask_out').get('character')
            size=args.get(column).get('mask_out').get('from')
            mask_out(data_frame, column, with_,character, size)
        elif 'set_null' in args.get(column):
            set_null_value = args.get(column).get('set_null').lower()
            set_null_value = True if set_null_value == 'true' else False
            if set_null_value:
                set_null(data_frame,column)


def concatenate(data_frame, number, args=None):

    dcols = [f for f in data_frame.columns if f.startswith("concatenate")]
    for column_name, data_frame_col_name in zip(args, dcols):
        template = args.get(column_name).get('template', None)
        if template is None:
            raise AttributeError(f"No value found for attribute `template` in `advanced.concatenate` schema entry!")

        text_in_brackets = re.findall('{(.+?)}', template)
        for entry in text_in_brackets:
            if entry not in data_frame.columns:
                raise IndexError(f"No column with name `{entry}` found in the schema!")
            template = template.replace(entry, f"x['{entry}']")
        template = "f\"" + template + "\""
        data_frame[data_frame_col_name] = data_frame.agg(lambda x: eval(template), axis=1)
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)

