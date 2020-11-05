#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import os

from airflow import LoggingMixin


def check_mandatory_field(stream, name):
    result = True
    if 'number' not in stream:
        LoggingMixin().log.error(f"AttributeError: `number` attribute not found in {name}.py")
        result = False
    else:
        if not isinstance(stream['number'], int):
            LoggingMixin().log.error(f"ValueError: `number` must be integer in {name}.py")
            result = False

    # if 'format' not in stream:
    #     LoggingMixin().log.error(f"AttributeError: `format` attribute not found in {name}.py")
    #     result = False

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


def check_schema_attribs(schema, name):
    stored_field_names=[]
    result = True
    for sch in schema:
        if not isinstance(sch, dict):
            LoggingMixin().log.error(f'TypeError: entries in `synthetic` are not of type `dictionary` in {name}.py')
            result = False
        else:
            if 'field_name' not in sch:
                LoggingMixin().log.error(
                    f'AttributeError: `field_name` attribute not present in `synthetic` in {name}.py')
                result = False
            if 'type' not in sch:
                LoggingMixin().log.error(f'AttributeError: `type` attribute not present in `synthetic` in {name}.py')
                result = False

            #means field_name is present now
            # check for duplicates field_names in synthetic, because dataframe cannot hold two columns of same name.
            field_name = sch.get('field_name')
            if field_name in stored_field_names:
                LoggingMixin().log.error(f'Duplicate field_name `{field_name}` found in `synthetic` attribute for {name}.py')
            else:
                stored_field_names.append(field_name)

    return result


def check_schema_type(stream, name):
    result = True
    schema = stream.get('synthetic')  # "schema" is now "synthetic"
    if schema is not None:
        if not isinstance(schema, list):
            LoggingMixin().log.error(f"TypeError: `synthetic` must be of type `list` in {name}.py")
            result = False
        else:
            if len(schema) > 0:
                result = check_schema_attribs(schema, name)
            else:
                LoggingMixin().log.error(f"`synthetic` cannot be empty in {name}.py")
                result = False
    else:
        LoggingMixin().log.warn(f"`synthetic` attribute not found  in {name}.py")

    return result


def check_internal_attributes(key, params, name, parent):
    # [{'connection': 'modeling', 'delimiter': ','}, {'connection': 'health', 'delimiter': ','}]
    result = True
    for p in params:
        if not isinstance(p, dict):
            LoggingMixin().log.error(
                f'TypeError: In `{parent}`, `{key}` values is not of type `dictionary` in {name}.py')
            result = False
        else:
            # connection:modeling
            if 'connection' not in p:
                LoggingMixin().log.error(
                    f'AttributeError:In `{parent}`, `connection` attribute not present in `{key}` in {name}.py')
                result = False

            # POSTGRES
            if key == 'postgres':
                if 'connection' not in p:
                    LoggingMixin().log.error(
                        f'AttributeError:In `{parent}`, `connection` attribute not present in `{key}` in {name}.py')
                    result = False
                if 'table' not in p:
                    LoggingMixin().log.error(
                        f'AttributeError:In `{parent}`, `table` attribute not present in `{key}` in {name}.py')
                    result = False

            # MYSQL
            if key == 'mysql':
                if 'connection' not in p:
                    LoggingMixin().log.error(
                        f'AttributeError:In `{parent}`, `connection` attribute not present in `{key}` in {name}.py')
                    result = False
                if 'table' not in p:
                    LoggingMixin().log.error(
                        f'AttributeError:In `{parent}`, `table` attribute not present in `{key}` in {name}.py')
                    result = False
            # MSSQL
            if key == 'mssql':
                if 'connection' not in p:
                    LoggingMixin().log.error(
                        f'AttributeError:In `{parent}`, `connection` attribute not present in `{key}` in {name}.py')
                    result = False
                if 'table' not in p:
                    LoggingMixin().log.error(
                        f'AttributeError:In `{parent}`, `table` attribute not present in `{key}` in {name}.py')
                    result = False
        # SFTP
        if key == 'sftp':
            if 'connection' not in p:
                LoggingMixin().log.error(
                    f'AttributeError:In`{parent}`, `connection` attribute not present in `{key}` in {name}.py')
                result = False
            if 'file' not in p:
                LoggingMixin().log.error(
                    f'AttributeError:In `{parent}`, `file` attribute not present in `{key}` in {name}.py')
                result = False
        # ServiceNow
        if key == 'servicenow':
            if 'connection' not in p:
                LoggingMixin().log.error(
                    f'AttributeError:In`{parent}`, `connection` attribute not present in `{key}` in {name}.py')
                result = False
            if 'table' not in p:
                LoggingMixin().log.error(
                    f'AttributeError:In `{parent}`, `table` attribute not present in `{key}` in {name}.py')
                result = False
    return result


def check_source(stream, name):
    result = True

    if 'source' in stream:
        SOURCE = stream.get('source')
        if not isinstance(SOURCE, dict):
            LoggingMixin().log.error(f'TypeError: `source` is not of type `dictionary` in {name}.py')
            result = False
        else:
            if len(SOURCE) > 0:
                for key in SOURCE:
                    if not isinstance(SOURCE.get(key), list):
                        LoggingMixin().log.error(f'TypeError:In `source`, `{key}`  is not of type `list` in {name}.py')
                        result = False
                    else:
                        result = check_internal_attributes(key, SOURCE.get(key), name, parent='source')
            else:
                LoggingMixin().log.error(f"`source` cannot be empty in {name}.py")
                result = False
    else:
        LoggingMixin().log.warn(f'`source` is not present  in {name}.py')

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


def check_encrypt_type(encryption, name):
    result = True
    if encryption is not None:
        if 'type' not in encryption:
            LoggingMixin().log.error(
                f'AttributeError: `type` attribute not present in `encryption` in {name}.py')
            result = False
        if 'key' not in encryption:
            LoggingMixin().log.error(
                f'AttributeError: `key` attribute not present in `encryption` in {name}.py')
            result = False

        encrypt_type_value = encryption.get('type')
        if encrypt_type_value not in ('fernet', 'caesar', 'monoaplha', 'onetimepad', 'aes'):
            LoggingMixin().log.error(
                f'`type` in encrypt can be `fernet` / `caesar` / `monoaplha` / `onetimepad` / `aes`')
            result = False
    else:
        LoggingMixin().log.warn(f"`encryption` is not present for `encrypt` in {name}.py")
    return result


def check_encrypt(stream, name):
    result = True
    if 'source' in stream:
        encrypt = stream.get('encrypt')
        encryption = stream.get('encryption')
        if encrypt is not None:
            if not isinstance(encrypt, (set, list)):
                LoggingMixin().log.error(f'TypeError: `encrypt` is not of type `set or list` in {name}.py')
                result = False
            else:
                result = check_encrypt_type(encryption, name)
    return result


def check_shuffle(stream, name):
    result = True
    if 'source' in stream:
        shuffle = stream.get('shuffle')
        if shuffle is not None:
            if not isinstance(shuffle, (list, set)):
                LoggingMixin().log.error(f'TypeError: `shuffle` is not of type `set or list` in {name}.py')
                result = False
    return result


def check_nullying(stream, name):
    result = True
    if 'source' in stream:
        nullying = stream.get('nullying')
        if nullying is not None:
            if not isinstance(nullying, (set, list)):
                LoggingMixin().log.error(f'TypeError: `nullying` is not of type  `set or list` in {name}.py')
                result = False
    return result


def check_delete(stream, name):
    result = True
    if 'source' in stream:
        delete = stream.get('delete')
        if delete is not None:
            if not isinstance(delete, (set, list)):
                LoggingMixin().log.error(f'TypeError: `delete` is not of type  `set or list` in {name}.py')
                result = False
    return result


def check_mask_out_atrributes(mask, name):
    result = True
    if mask is not None:
        if 'with' not in mask or 'characters' not in mask or 'from' not in mask:
            LoggingMixin().log.error(
                f"AttributeError: `with`,`characters` and  `from` are mandatory for mask_out in  {name}.py")
            result = False
        else:

            if not isinstance(mask['characters'], int):
                LoggingMixin().log.error("ValueError: `characters` in `mask_out` must be integer")
                result = False

            if not isinstance(mask['with'], str):
                LoggingMixin().log.error("ValueError: `with` in `mask_out` must be string")
                result = False

            if mask['from'] not in ('start', 'mid', 'end'):
                LoggingMixin().log.error("ValueError: `from` in `mask_out` must be `start` or `mid` or `end`")
                result = False
    else:
        LoggingMixin().log.warn(f"`mask` is not present for `mask_out` in {name}.py")

    return result


def check_mask_out(stream, name):
    result = True
    if 'source' in stream:
        mask_out = stream.get('mask_out')
        mask = stream.get('mask')
        if mask_out is not None:
            if not isinstance(mask_out, (set, list)):
                LoggingMixin().log.error(f'TypeError: `mask_out` is not of type `set or list` in {name}.py')
                result = False
            else:
                result = check_mask_out_atrributes(mask, name)
    return result


def check_destination(stream, name):
    result = True
    if 'destination' in stream:
        DESTINATION = stream.get('destination')
        if not isinstance(DESTINATION, dict):
            LoggingMixin().log.error(f'TypeError: `destination` is not of type `dictionary` in {name}.py')
            result = False
        else:
            result = True
            if len(DESTINATION) > 0:
                for key in DESTINATION:
                    if not isinstance(DESTINATION.get(key), list):
                        LoggingMixin().log.error(
                            f'TypeError: In `destination`, `{key}`  is not of type `list` in {name}.py')
                        result = False
                    else:
                        result = check_internal_attributes(key, DESTINATION.get(key), name, parent='destination')
            else:
                LoggingMixin().log.error(f"`destination` cannot be empty in {name}.py")
                result = False
    else:
        LoggingMixin().log.warn(f'`destination` is not present  in {name}.py')
    return result


def check_output_schema(stream, name):
    result = True
    if 'output_schema' in stream:
        output_schema = stream.get('output_schema')
        if len(output_schema) > 0:
            if not isinstance(output_schema, (dict, list, set)):
                LoggingMixin().log.error(
                    f'TypeError: `output_schema` is not of type `dictionary or set or list` in {name}.py')
                result = False
        else:
            LoggingMixin().log.error(f"`output_schema` cannot be empty in {name}.py")
            result = False

    else:
        LoggingMixin().log.error(f"AttributeError: `output_schema` attribute not found in {name}.py")
        result = False

    return result


class Validation:

    @staticmethod
    def validate(stream, name):
        # all([True, False, True])
        return all(
            [
                check_mandatory_field(stream, name),
                check_schema_type(stream, name),
                check_source(stream, name),
                check_substitute(stream, name),
                check_encrypt(stream, name),
                check_shuffle(stream, name),
                check_nullying(stream, name),
                check_delete(stream, name),
                check_mask_out(stream, name),
                check_destination(stream, name),
                check_output_schema(stream, name)
            ]
        )
