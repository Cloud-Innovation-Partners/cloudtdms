#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
import re
import os
import random
import pandas as pd
from system.cloudtdms.providers.advanced import masking
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


def custom_file(data_frame, number, args=None):

    data_path = f"{os.path.dirname(get_airflow_home())}/user-data/.__temp__"
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

        if 'encrypt' in args.get(column_name):
            key=args.get(column_name).get('encrypt').get('key')
            type=args.get(column_name).get('encrypt').get('type','fernet').lower()
            masking.encrypt(data_frame, column, key, type)
        elif 'shuffle' in args.get(column_name):
            shuffle_value= str(args.get(column_name).get('shuffle')).lower()
            shuffle_value = True if shuffle_value == 'true' else False
            if shuffle_value:
                masking.shuffle(data_frame, column)
        elif 'mask_out' in args.get(column_name):
            with_=args.get(column_name).get('mask_out').get('with')
            character=args.get(column_name).get('mask_out').get('characters')
            size=args.get(column_name).get('mask_out').get('from')
            masking.mask_out(data_frame, column, with_,character, size)
        elif 'set_null' in args.get(column_name):
            set_null_value = str(args.get(column_name).get('set_null')).lower()
            set_null_value = True if set_null_value == 'true' else False
            if set_null_value:
                masking.set_null(data_frame,column)


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

