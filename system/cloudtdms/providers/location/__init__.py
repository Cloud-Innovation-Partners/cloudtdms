#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from faker import Faker
import random
import string
import pandas as pd
import os


def location(data_frame, number, args):
    field_names = {}
    for k in args:
        if k.split('-$-', 2)[1] not in field_names:
            field_names[k.split('-$-', 2)[1]] = {k.split('-$-', 2)[0]: args.get(k)}
        else:
            field_names[k.split('-$-', 2)[1]][k.split('-$-', 2)[0]] = args.get(k)

    columns = field_names.keys()

    df = pd.read_csv(f"{os.path.dirname(__file__)}/airport.csv")

    # {'phone_number': {'phone': {'format': '#-(###)-###-####'}}, 'muncipality': {'muncipality': {}},
    #  'longitude': {'longitude': {}}, 'latitude': {'latitude': {}}, 'country': {'country': {}, 'country2': {}},
    #  'city': {'city': {}}, 'airport': {'airport': {}}}

    if 'phone_number' in columns:
            phone_number(data_frame, number, field_names.get('phone_number'))

    cols=['airport','latitude','longitude','municipality','country','country_code','city','state','postal_code']
    t_data_frame = pd.DataFrame(tuple(df[cols].iloc[random.randint(0, len(df) - 1)] for _ in range(number)))
    t_data_frame.reset_index(drop=True, inplace=True)
    data_frame[cols] = t_data_frame

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

country_calling_codes = [
    '+93', '+358 18', '+355', '+213', '+1 684', '+376', '+244', '+1 264',
    '+1 268', '+54', '+374', '+297', '+247', '+61', '+672 1', '+672', '+43',
    '+994', '+1 242', '+973', '+880', '+1 246', '+1 268', '+375', '+32',
    '+501', '+229', '+1 441', '+975', '+591', '+599 7', '+387', '+267',
    '+55', '+246', '+1 284', '+673', '+359', '+226', '+257', '+855', '+237',
    '+1', '+238', '+599 3', '+599 4', '+599 7', '+1 345', '+236', '+235',
    '+64', '+56', '+86', '+61 89164', '+61 89162', '+57', '+269', '+242',
    '+243', '+682', '+506', '+385', '+53', '+599 9', '+357', '+420',
    '+45', '+246', '+253', '+1 767', '+1 809', '+1 829', '+1 849', '+670',
    '+56', '+593', '+20', '+503', '+881 2', '+881 3', '+882 13', '+240',
    '+291', '+372', '+268', '+251', '+500', '+298', '+679', '+358',
    '+33', '+596', '+594', '+689', '+241', '+220', '+995', '+49',
    '+233', '+350', '+881', '+881 8', '+881 9', '+30', '+299', '+1 473',
    '+590', '+1 671', '+502', '+44 1481', '+44 7781', '+44 7839', '+44 7911', '+224',
    '+245', '+592', '+509', '+504', '+852', '+36', '+354', '+881 0',
    '+881 1', '+91', '+62', '+870', '+800', '+882', '+883', '+979',
    '+808', '+98', '+964', '+353', '+881 6', '+881 7', '+44 1624', '+44 7524',
    '+44 7624', '+44 7924', '+972', '+39', '+225', '+1 876', '+47 79', '+81',
    '+44 1534', '+962', '+7 6', '+7 7', '+254', '+686', '+850', '+82',
    '+383', '+965', '+996', '+856', '+371', '+961', '+266', '+231',
    '+218', '+423', '+370', '+352', '+853', '+261', '+265', '+60',
    '+960', '+223', '+356', '+692', '+596', '+222', '+230', '+262 269',
    '+262 639', '+52', '+691', '+1 808', '+373', '+377', '+976', '+382',
    '+1 664', '+212', '+258', '+95', '+374 47', '+374 97', '+264', '+674',
    '+977', '+31', '+1 869', '+687', '+64', '+505', '+227', '+234',
    '+683', '+672 3', '+389', '+90 392', '+44 28', '+1 670', '+47', '+968',
    '+92', '+680', '+970', '+507', '+675', '+595', '+51', '+63',
    '+64', '+48', '+351', '+1 787', '+1 939', '+974', '+262', '+40',
    '+7', '+250', '+599 4', '+590', '+290', '+1 869', '+1 758', '+590',
    '+508', '+1 784', '+685', '+378', '+239', '+966', '+221', '+381',
    '+248', '+232', '+65', '+599 3', '+1 721', '+421', '+386', '+677',
    '+252', '+27', '+500', '+995 34', '+211', '+34', '+94', '+249',
    '+597', '+47 79', '+46', '+41', '+963', '+886', '+992', '+255',
    '+888', '+66', '+882 16', '+228', '+690', '+676', '+373 2', '+373 5',
    '+1 868', '+290 8', '+216', '+90', '+993', '+1 649', '+688', '+256',
    '+380', '+971', '+44', '+1', '+878', '+598', '+1 340', '+998',
    '+678', '+39 06 698', '+379', '+58', '+84', '+1 808', '+681', '+967',
    '+260', '+255 24', '+263',
]


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
    if format.startswith('+'):
        code = country_code
        code = code.replace(' ', '')
        # format=format[2:]
        cell_number = list(code + cell_number)[1:]
    else:
        cell_number = list(code + cell_number)
    for i in range(len(cell_number)):
        format = format.replace('#', str(cell_number[i]), 1)
    formatted_cell_number = format
    return formatted_cell_number


# {'phone': {'format': '#-(###)-###-####'}}
def phone_number(data_frame, number, args=None):
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
            length = len(format.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', ''))
        else:
            format = '##########'
            length = len(format)
        for _ in range(number):
            random.shuffle(country_calling_codes)
            random.shuffle(digits)
            cell_number = ''.join(digits[:length])
            formatted_cell_number = replace_hashes(format, cell_number, country_calling_codes[0])
            cell_number_list.append(formatted_cell_number)
        data_frame[data_frame_col_name] = cell_number_list[:number]
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


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

def timezones(number):
    """
        Generator function for timezones
        :param number: Number of records to generate
        :type int
        :return: list
    """
    faker = Faker()
    return [faker.timezone() for _ in range(number)]
