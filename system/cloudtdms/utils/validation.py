#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import os

from airflow import LoggingMixin


def check_mandatory_field(stream, name):
    result=True
    if 'number' not in stream:
        LoggingMixin().log.error(f"AttributeError: `number` attribute not found in {name}.py")
        result=False
    else:
        if not isinstance(stream['number'], int):
            LoggingMixin().log.error(f"ValueError: `number` must be integer in {name}.py")
            result = False

    if 'format' not in stream:
        LoggingMixin().log.error(f"AttributeError: `format` attribute not found in {name}.py")
        result = False

    if 'title' not in stream:
        LoggingMixin().log.error(f"AttributeError: `title` attribute not found in {name}.py")
        result = False
    else:
        title_value = stream.get('title')
        if len(title_value) == 0:
            LoggingMixin().log.error("ValueError: `title` cannot be empty or None")
            result = False
    if 'frequency' not in stream:
        LoggingMixin().log.error(f"AttributeError: `frequency` attribute not found in {name}.py")
        result = False
    else:
        frequency_value = stream['frequency']
        if frequency_value not in ('once', 'hourly', 'daily', 'monthly'):
            LoggingMixin().log.error(
                f"ValueError: Invalid value `{frequency_value}` for `frequency` attribute in {name}.py")
            result = False
    return  result


def check_stream_type(stream, name):
    if not isinstance(stream, dict):
        LoggingMixin().log.error(f"TypeError: `stream` is not of type `dictionary` in {name}.py")


def check_schema_attribs(schema, name):
    result=True
    for sch in schema:
        if not isinstance(sch, dict):
            LoggingMixin().log.error(f'TypeError: entries in `schema` are not of type `dictionary` in {name}.py')
            result=False
        else:
            if 'field_name' not in sch:
                LoggingMixin().log.error(f'AttributeError: `field_type` attribute not present in `schema` in {name}.py')
                result=False
            if 'type' not in sch:
                LoggingMixin().log.error(f'AttributeError: `type` attribute not present in `schema` in {name}.py')
                result=False
    return  result


def check_schema_type(stream, name):
    result=True
    schema = stream.get('schema')
    if schema is not None:
        if not isinstance(schema, list):
            LoggingMixin().log.error(f"TypeError: `schema` must be of type `list` in {name}.py")
            result=False
        else:
            result=check_schema_attribs(schema, name)
    else:
        pass

    return result


def set_default_format(stream, name):
    if 'format' in stream:
        format = stream['format']
        if format != 'csv':
            stream['format'] = 'csv'

    return stream


def check_source(stream, name):
    result=True
    if 'source' not in stream:
        LoggingMixin().log.error(f'AttributeError: `source` attribute not found in {name}.py')
        result=True
    else:
        # /home/user/AFW/cloudtdms/system/cloudtdms/utils/validation.py
        # /home/user/AFW/cloudtdms/user-data
        source_value = stream.get('source')
        splitted = str(__file__).split('/')
        splitted = splitted[:-4]
        joined_path = '/'.join(splitted) + '/user-data/' + source_value + '.csv'
        if not os.path.exists(joined_path):
            LoggingMixin().log.error(f'ValueError: File {source_value} not found')
            result=False
    return result


def check_substitute(stream, name):
    result=True
    if 'source' in stream:
        subst = stream.get('substitute')
        if subst is not None:
            if not isinstance(subst, dict):
                LoggingMixin().log.error(f'TypeError: `substitute` is not of type `dictionary` in {name}.py')
                result=False
            else:
                for sub in subst:
                    sub_value = subst[sub]
                    if not isinstance(sub_value, dict):
                        LoggingMixin().log.error(
                            f'TypeError: entries in `substitute` are not of type `dictionary` in {name}.py')
                        result=False
                    else:
                        if 'type' not in sub_value:
                            LoggingMixin().log.error(
                                f'AttributeError: `type` attribute not present in `substitute` in {name}.py')
                            result=False
    return result


def check_encrypt_type(encrypt):
    encrypt_type_value=encrypt.get('type')
    if encrypt_type_value not in ('fernet', 'caesar', 'monoaplha', 'onetimepad', 'aes'):
        LoggingMixin().log.error(f'`type` in encrypt can be `fernet` / `caesar` / `monoaplha` / `onetimepad` / `aes`')


def check_encrypt(stream, name):
    result=True
    if 'source' in stream:
        encrypt = stream.get('encrypt')
        if encrypt is not None:
            if not isinstance(encrypt, dict):
                LoggingMixin().log.error(f'TypeError: `encrypt` is not of type `dictionary` in {name}.py')
                result=False
            else:
                encrypt_cols = encrypt.get('columns')
                if not isinstance(encrypt_cols, list) and encrypt_cols is not None:
                    LoggingMixin().log.error(f'TypeError: `columns` in `encrypt` is not of type `list` in {name}.py')
                    result=False
                check_encrypt_type(encrypt)
    return result

def check_shuffle(stream, name):
    result=True
    if 'source' in stream:
        shuffle = stream.get('shuffle')
        if shuffle is not None:
            if not isinstance(shuffle, list):
                LoggingMixin().log.error(f'TypeError: `shuffle` is not of type `list` in {name}.py')
                result= False
    return result


def check_nullying(stream, name):
    result=True
    if 'source' in stream:
        nullying = stream.get('nullying')
        if nullying is not None:
            if not isinstance(nullying, list):
                LoggingMixin().log.error(f'TypeError: `nullying` is not of type `list` in {name}.py')
                result=False
    return result


def check_delete(stream, name):
    result=True
    if 'source' in stream:
        delete = stream.get('delete')
        if delete is not None:
            if not isinstance(delete, list):
                LoggingMixin().log.error(f'TypeError: `delete` is not of type `list` in {name}.py')
                result=False
    return result


def check_arrtibutes(mask_out_value):
    if not isinstance(mask_out_value['characters'], int):
        LoggingMixin().log.error("ValueError: `characters` in `mask_out` must be integer")

    if not isinstance(mask_out_value['with'], str):
        LoggingMixin().log.error("ValueError: `with` in `mask_out` must be string")

    if mask_out_value['from'] not in ('start','mid','end'):
        LoggingMixin().log.error("ValueError: `from` in `mask_out` must be `start` or `mid` or `end`")


def check_mask_out(stream, name):
    if 'source' in stream:
        mask_out = stream.get('mask_out')
        if mask_out is not None:
            if not isinstance(mask_out, dict):
                LoggingMixin().log.error(f'TypeError: `mask_out` is not of type `dictionary` in {name}.py')
            for mask in mask_out:
                mask_out_value = mask_out[mask] # {'with': 'x', 'characters': 4, 'from': 'start'}
                if not isinstance(mask_out_value, dict):
                    LoggingMixin().log.error(
                        f'TypeError: Entries in `mask_out` are not of type `dictionary` in {name}.py')
                else:
                    if 'with' not in mask_out_value or 'characters' not in mask_out_value or 'from' not in mask_out_value:
                        LoggingMixin().log.error(
                            f"AttributeError: `with`,`characters` and  `from` are mandatory for mask_out in  {name}.py")
                    else:
                        check_arrtibutes(mask_out_value)