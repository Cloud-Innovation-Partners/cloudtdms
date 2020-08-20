#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
from airflow import LoggingMixin
from faker import Faker
import random
import string
import pandas as pd
import os


def location(data_frame, number, args):
    field_names = {}
    for k in args:
        if k=='locale':
            continue
        if k.split('-$-', 2)[1] not in field_names:
            field_names[k.split('-$-', 2)[1]] = {k.split('-$-', 2)[0]: args.get(k)}
        else:
            field_names[k.split('-$-', 2)[1]][k.split('-$-', 2)[0]] = args.get(k)

    columns = field_names.keys()

    locale=args.get('locale')
    if locale is not None:
        if os.path.exists(f"{os.path.dirname(__file__)}/{locale}"):
            df = pd.read_csv(f"{os.path.dirname(__file__)}/{locale}/airport.csv")
        else:
            LoggingMixin().log.error(f"InvalidValue found for attribute `locale` in schema.")
            df = pd.read_csv(f"{os.path.dirname(__file__)}/airport.csv")
    else:
        df = pd.read_csv(f"{os.path.dirname(__file__)}/airport.csv")

    # {'phone_number': {'phone': {'format': '#-(###)-###-####'}}, 'muncipality': {'muncipality': {}},
    #  'longitude': {'longitude': {}}, 'latitude': {'latitude': {}}, 'country': {'country': {}, 'country2': {}},
    #  'city': {'city': {}}, 'airport': {'airport': {}}}



    cols=['airport','latitude','longitude','municipality','country','country_code','city','state','postal_code','calling_code', 'timezone']
    t_data_frame = pd.DataFrame(tuple(df[cols].iloc[random.randint(0, len(df) - 1)] for _ in range(number)))
    t_data_frame.reset_index(drop=True, inplace=True)
    data_frame[cols] = t_data_frame

    # here data_frame contains the calling code column
    if 'phone_number' in columns:
            phone_number(data_frame, number, field_names.get('phone_number'))

    #here data_frame contains the country_code column
    if 'address' in columns:
        address(data_frame, number, field_names.get('address'))


    # name,latitude,longitude,municipality,country,region,cities,states,postal_codes
    for col in ['airport','latitude','longitude','municipality','country','country_code','city','state','postal_code']:
        if col not in columns:
            data_frame.drop(col, inplace=True, axis=1)

    # {'country': {'country': {}, 'country2': {}}
    for item in field_names:

        count = len(field_names[item])
        column_names = list(field_names[item].keys())
        if count > 0:
            if item in ('address', 'phone_number'):
                for label in column_names[1:]:
                    random.shuffle(data_frame[label])
            else:
                data_frame.rename(columns={item:column_names[0]}, inplace=True)
                for i in range(1,len(column_names)):
                    data_frame[f"{item}{i}"] = data_frame[column_names[0]]
                    data_frame.rename(columns={f"{item}{i}" : column_names[i]}, inplace=True)
                    random.shuffle(data_frame[column_names[i]])

def country(number):
    """
        Generator function for countries
        :param number: Number of records to generate
        :type int
        :return: list
    """
    raise NotImplemented

def state(number):
    """
        Generator function for countries
        :param number: Number of records to generate
        :type int
        :return: list
    """
    raise NotImplemented


def city(number):
    """
     Generator function for cities
     :param number: Number of records to generate
     :type int
     :return: list
     """
    raise NotImplemented


def latitude(number):
    """
        Generator function for latitude
        :param number: Number of records to generate
        :type int
        :return: list
    """
    raise NotImplemented


def longitude(number):
    """
        Generator function for longitude
        :param number: Number of records to generate
        :type int
        :return: list
    """
    raise NotImplemented


def replace_hashes(format, cell_number, country_code):
    code = ''
    if format.startswith('+#'):
        code = country_code
        code = code.replace(' ', '')
        # format=format[2:]
        format = format.replace('+#', '+' + code, 1)
        cell_number = list(cell_number)
    elif format.startswith('#-'):
        code = country_code
        code = code.replace(' ', '')
        # format=format[2:]
        format = format.replace('#-', '+' + code + '-', 1)
        cell_number = list(cell_number)
    else:
        cell_number = list(code + cell_number)

    for i in range(len(cell_number)):
        format = format.replace('#', str(cell_number[i]), 1)
        formatted_cell_number = format
    return formatted_cell_number


# {'phone': {'format': '#-(###)-###-####'}}
def phone_number(data_frame, number, args=None):
    print(data_frame.columns)
    """
     Generator function for phone numbers
     :param number: Number of records to generate
     :type int
     :param args: schema attribute values
     :type dict
     :return: list
     """
    cell_number_list = []
    digits = list(string.digits * 3)

    dcols = [f for f in data_frame.columns if f.startswith("phone_number")]
    for column_name, data_frame_col_name in zip(args, dcols):
        if args is not None:
            format = args.get(column_name).get('format', '##########')
            length = len(format.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+#', '').replace('#-', ''))
        else:
            format = '##########'
            length = len(format)
        for _,code in zip(range(number),data_frame['calling_code']):
            # random.shuffle(country_calling_codes)
            code=str(int(code))
            random.shuffle(digits)
            cell_number = ''.join(digits[:length])
            formatted_cell_number = replace_hashes(format, cell_number, code)
            cell_number_list.append(formatted_cell_number)
        data_frame[data_frame_col_name] = cell_number_list[:number]
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)

    if 'calling_code' in data_frame.columns:
        data_frame.drop('calling_code', inplace=True, axis=1)


def postal_code(number):
    """
    Generator function for post codes
    :param number: Number of records to generate
    :type int
    :return: list
    """
    raise NotImplemented


def country_code(number):
    """
        Generator function for country codes
        :param number: Number of records to generate
        :type int
        :return: list
    """
    raise NotImplemented

def address(data_frame, number, args=None):
    addresses=[]
    df_region=data_frame['country_code']
    faker = Faker()

    dcols = [f for f in data_frame.columns if f.startswith("address")]
    for column_name, data_frame_col_name in zip(args, dcols):
        for i in range(number):
            address=faker.address()
            address = address.replace('\n', ' ')

            if ',' not in address:
                address = address.split(' ')
                total = len(address)
                address[total - 2] = ', ' + address[total - 2]
                address = ' '.join(address)

            # print(f'OLD-- {address}')
            address=address.split(',',2)
            address[1] = " "+str(df_region[i])+" " + address[1].strip().split(' ')[1]
            address=''.join(address)
            # print(f'NEW-- {address}')
            addresses.append(address)
        data_frame[data_frame_col_name] = addresses[:number]
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)




def airport(number):
    raise NotImplemented

def municipality(number):
    raise NotImplemented

def timezone(number):
    """
        Generator function for timezones
        :param number: Number of records to generate
        :type int
        :return: list
    """
    raise NotImplemented
