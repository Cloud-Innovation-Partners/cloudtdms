#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import hashlib

import numpy as np
import base64
import hashlib
import onetimepad
from Crypto.Cipher import AES
from airflow.utils.log.logging_mixin import LoggingMixin
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


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
    if type(key) is str:
        key = sum(map(lambda x: ord(str(x)), key))
    else:
        key = int(key)
    record = str(record)
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
    for i in str(record):
        updated_record+= monoalpha_cipher_list.get(i,i)
    return updated_record

def onetime(record, key):
    record =str(record)
    key=str(key)
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
    elif type == 'monoalpha':
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
