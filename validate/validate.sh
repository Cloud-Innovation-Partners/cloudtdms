#!/usr/bin/env python
#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import os
import argparse
import importlib
import sys
from airflow.utils.log.logging_mixin import LoggingMixin

def check_mandatory_field(stream, name):
    result = True
    if 'number' not in stream:
        LoggingMixin().log.error(f"AttributeError: `number` attribute not found in {name}.py")
        result = False
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
    return result


def check_stream_type(stream, name):
    if not isinstance(stream, dict):
        LoggingMixin().log.error(f"TypeError: `stream` is not of type `dictionary` in {name}.py")


def check_schema_attribs(schema, name):
    result = True
    for sch in schema:
        if not isinstance(sch, dict):
            LoggingMixin().log.error(f'TypeError: entries in `schema` are not of type `dictionary` in {name}.py')
            result = False
        else:
            if 'field_name' not in sch:
                LoggingMixin().log.error(f'AttributeError: `field_name` attribute not present in `schema` in {name}.py')
                result = False
            if 'type' not in sch:
                LoggingMixin().log.error(f'AttributeError: `type` attribute not present in `schema` in {name}.py')
                result = False
    return  result


def check_schema_type(stream, name):
    result = True
    schema = stream.get('schema')
    if schema is not None:
        if not isinstance(schema, list):
            LoggingMixin().log.error(f"TypeError: `schema` must be of type `list` in {name}.py")
            result = False
        else:
            result = check_schema_attribs(schema, name)
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
    result = True
    masking_attributes = ['encrypt', 'substitute', 'nullying', 'delete', 'mask_out', 'shuffle']
    if 'source' not in stream and any(item in stream for item in masking_attributes):
        LoggingMixin().log.error(f'AttributeError: `source` attribute not found in {name}.py')
        result = False

    return result


def check_substitute(stream, name):
    result = True
    if 'source' in stream:
        subst = stream.get('substitute')
        if subst is not None:
            if not isinstance(subst, dict):
                LoggingMixin().log.error(f'TypeError: `substitute` is not of type `dictionary` in {name}.py')
                result = False
            else:
                for sub in subst:
                    sub_value = subst[sub]
                    if not isinstance(sub_value, dict):
                        LoggingMixin().log.error(
                            f'TypeError: entries in `substitute` are not of type `dictionary` in {name}.py')
                        result = False
                    else:
                        if 'type' not in sub_value:
                            LoggingMixin().log.error(
                                f'AttributeError: `type` attribute not present in `substitute` in {name}.py')
                            result = False
    return result


def check_encrypt_type(encrypt):
    encrypt_type_value=encrypt.get('type')
    if encrypt_type_value not in ('fernet', 'caesar', 'monoaplha', 'onetimepad', 'aes'):
        LoggingMixin().log.error(f'`type` in encrypt can be `fernet` / `caesar` / `monoaplha` / `onetimepad` / `aes`')


def check_encrypt(stream, name):
    result = True
    if 'source' in stream:
        encrypt = stream.get('encrypt')
        if encrypt is not None:
            if not isinstance(encrypt, dict):
                LoggingMixin().log.error(f'TypeError: `encrypt` is not of type `dictionary` in {name}.py')
                result = False
            else:
                encrypt_cols = encrypt.get('columns')
                if not isinstance(encrypt_cols, list) and encrypt_cols is not None:
                    LoggingMixin().log.error(f'TypeError: `columns` in `encrypt` is not of type `list` in {name}.py')
                    result = False
                check_encrypt_type(encrypt)
    return result


def check_shuffle(stream, name):
    result = True
    if 'source' in stream:
        shuffle = stream.get('shuffle')
        if shuffle is not None:
            if not isinstance(shuffle, list):
                LoggingMixin().log.error(f'TypeError: `shuffle` is not of type `list` in {name}.py')
                result =  False
    return result


def check_nullying(stream, name):
    result = True
    if 'source' in stream:
        nullying = stream.get('nullying')
        if nullying is not None:
            if not isinstance(nullying, list):
                LoggingMixin().log.error(f'TypeError: `nullying` is not of type `list` in {name}.py')
                result = False
    return result


def check_delete(stream, name):
    result = True
    if 'source' in stream:
        delete = stream.get('delete')
        if delete is not None:
            if not isinstance(delete, list):
                LoggingMixin().log.error(f'TypeError: `delete` is not of type `list` in {name}.py')
                result = False
    return result


def check_attributes(mask_out_value):
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
                        check_attributes(mask_out_value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("FILENAME", type=str, help="cloudtdms python configuration file")
    args = parser.parse_args()

    # Argument
    module = args.FILENAME
    # check file exists

    if os.path.exists(module):
        if str(module)[-2:] != 'py':
            LoggingMixin().log.error("configuration must have .py extension")
            raise TypeError(module)

        LoggingMixin().log.info("Path : OK")
    else:
        raise FileNotFoundError(module)

    imodule = None

    # import configuration as module
    try:
        imodule = importlib.import_module(str(module)[:-3])
        LoggingMixin().log.info("SYNTAX : OK")

    except SyntaxError as se:
        LoggingMixin().log.error(f"SyntaxError: You configuration {se.filename} does not have valid syntax!")
        exit()

    except ImportError:
        LoggingMixin().log.error("ImportError: Invalid configuration found, unable to import", exc_info=True)
        exit()

    except Exception:
        LoggingMixin().log.error("Unknown Exception Occurred!", exc_info=True)
        exit()

    global stream

    # check it has 'STREAM' variable defined
    if imodule is not None and hasattr(imodule, 'STREAM'):
        if type(imodule.STREAM) is dict:
            stream = imodule.STREAM
            LoggingMixin().log.info("STREAM : OK")
            LoggingMixin().log.info("STREAM TYPE : OK")
        else:
            LoggingMixin().log.error("STREAM TYPE : FAIL")
            LoggingMixin().log.error("variable STREAM must be of type dict!")
            raise TypeError
    else:
        LoggingMixin().log.error("STREAM : FAIL")
        LoggingMixin().log.error("variable STREAM not defined!")
        raise AttributeError

    # check 'source' attribute is present
    source = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/user-data/{stream["source"]}.csv' if 'source' in stream else None

    if not check_mandatory_field(stream, module[:-3]):  # means false
        LoggingMixin().log.error("MANDATORY FIELDS : FAIL")
    else:
        LoggingMixin().log.info("MANDATORY FIELDS : OK")

    if not check_schema_type(stream, module[:-3]):
        LoggingMixin().log.error("SCHEMA TYPE : FAIL")
    else:
        LoggingMixin().log.info("SCHEMA TYPE : OK")

    if not check_source(stream, module[:-3]):
        LoggingMixin().log.error("SOURCE ATTRIBUTE : FAIL")
    else:
        LoggingMixin().log.info("SOURCE ATTRIBUTE : OK")

    if not check_delete(stream, module[:-3]):
        LoggingMixin().log.error("DELETE ATTRIBUTE : FAIL")
    else:
        LoggingMixin().log.info("DELETE ATTRIBUTE : OK")

    # columns in data-file
    all_columns = []
    if source is not None:
        try:
            with open(source, 'r') as f:
                columns = f.readline()
                columns = columns.replace('\n', '')
            all_columns = str(columns).split(',')
        except FileNotFoundError:
            LoggingMixin().log.error(f'ValueError: File {source} not found')
            exit()
    # get columns to delete
    delete = stream['delete'] if 'delete' in stream else []

    all_columns = list(set(all_columns) - set(delete))

    # check 'substitute' attribute is present along with 'source'
    if 'substitute' in stream and source is not None:
        if not check_substitute(stream, module[:-3]):
            LoggingMixin().log.error("SUBSTITUTE ATTRIBUTE : FAIL")
        else:
            LoggingMixin().log.info("SUBSTITUTE ATTRIBUTE : OK")

    # check 'encrypt' attribute is present along with 'source'

    if 'encrypt' in stream and source is not None:
        if not check_encrypt(stream, module[:-3]):
            LoggingMixin().log.error("ENCRYPT ATTRIBUTE : FAIL")
        else:
            LoggingMixin().log.info("ENCRYPT ATTRIBUTE : OK")

    # check 'mask_out' attribute is present along with 'source'

    if 'mask_out' in stream and source is not None:
        mask_outs = [k for k, v in stream['mask_out'].items() if k not in all_columns]
        if any(mask_outs):
            LoggingMixin().log.error("MASK OUT : FAIL")
            LoggingMixin().log.error(f"Columns {mask_outs} not found in data file {source}.csv")
        else:
            LoggingMixin().log.info("MASK OUT : OK")

    # check 'shuffle' attribute is present along with 'source'

    if 'shuffle' in stream and source is not None:
        shuffle = [v for v in stream['shuffle'] if v not in all_columns]
        if not check_shuffle(stream, module[:-3]) or any(shuffle):
            LoggingMixin().log.error("SHUFFLE ATTRIBUTE : FAIL")
            LoggingMixin().log.error(f"Columns {shuffle} not found in data file {source}.csv")
        else:
            LoggingMixin().log.info("ENCRYPT ATTRIBUTE : OK")

    # check 'nullying' attribute is present along with 'source'

    if 'nullying' in stream and source is not None:
        nullify = [v for v in stream['nullying'] if v not in all_columns]
        if not check_nullying(stream, module[:-3]):
            LoggingMixin().log.error("NULLYING ATTRIBUTE : FAIL")
            LoggingMixin().log.error(f"Columns {nullify} not found in data file {source}.csv")
        else:
            LoggingMixin().log.info("ENCRYPT ATTRIBUTE : OK")
