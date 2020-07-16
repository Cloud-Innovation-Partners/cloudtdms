#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from faker import Faker
import random
import string
import pandas as pd
import os

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
    faker = Faker()
    return [faker.country() for _ in range(number)]


def city(number):
    """
     Generator function for cities
     :param number: Number of records to generate
     :type int
     :return: list
     """
    faker = Faker()
    return [faker.city() for _ in range(number)]

def latitude(number):

    faker = Faker()
    return [str(faker.latitude()) for _ in range(number)]

def longitude(number):
    faker = Faker()
    return [str(faker.longitude()) for _ in range(number)]


def replace_hashes(format, cell_number, country_code):
    code=''
    if format.startswith('+'):
        code=country_code
        code=code.replace(' ','')
        # format=format[2:]
        cell_number=list(code+cell_number)[1:]
    else:
        cell_number = list(code + cell_number)
    for i  in range(len(cell_number)):
        format=format.replace('#',str(cell_number[i]),1)
    formatted_cell_number=format
    return formatted_cell_number


def phone_number(number, args=None):
    """
     Generator function for phone numbers
     :param number: Number of records to generate
     :type int
     :param args: schema attribute values
     :type dict
     :return: list
     """
    cell_number_list=[]
    digits = list(string.digits * 3)

    if args is not None:
        format=args.get('format','##########')
        length=len(format.replace(' ','').replace('-','').replace('(','').replace(')','').replace('+',''))
    else:
        format='##########'
        length=len(format)
    for _ in range(number):
        random.shuffle(country_calling_codes)
        random.shuffle(digits)
        cell_number=''.join(digits[:length])
        formatted_cell_number=replace_hashes(format,cell_number,country_calling_codes[0])
        cell_number_list.append(formatted_cell_number)
    return  cell_number_list

def post_code(number):
    """
    Generator function for post codes
    :param number: Number of records to generate
    :type int
    :return: list
    """
    faker = Faker()
    return [faker.postcode() for _ in range(number)]

def country_code(number):
    """
        Generator function for country codes
        :param number: Number of records to generate
        :type int
        :return: list
    """
    faker = Faker()
    return [faker.country_code() for _ in range(number)]

def address(number):
    """
        Generator function for addresses
        :param number: Number of records to generate
        :type int
        :return: list
    """
    faker = Faker()
    return [faker.address() for _ in range(number)]

def airport(number):
    """
        Generator function for airport names
        :param number: Number of records to generate
        :type int
        :return: list
    """
    path=os.path.dirname(__file__)+'/airpots.csv'
    df=pd.read_csv(path,usecols=['name'])
    length=len(df)
    return random.choices(df['name'],k=number) if length< number else df['name']

def muncipality(number):
    """
        Generator function for muncipality names
        :param number: Number of records to generate
        :type int
        :return: list
    """
    path = os.path.dirname(__file__) + '/airpots.csv'
    df = pd.read_csv(path, usecols=['Municipality'])
    length = len(df)
    return random.choices(df['Municipality'], k=number) if length < number else df['Municipality']

def timezones(number):
    """
        Generator function for timezones
        :param number: Number of records to generate
        :type int
        :return: list
    """
    faker = Faker()
    return [faker.timezone() for _ in range(number)]

