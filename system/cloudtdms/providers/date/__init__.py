#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service
from airflow import LoggingMixin
from faker import Faker
import  datetime
import random

def get_seperator(exp):
    for i in exp:
        if not i.isalnum():
            sep = i
    return sep

def split(exp):
    sep=get_seperator(exp)
    exp = exp.split(sep)
    return  exp


def validate(args):
    bool=True
    key, value=list(args.items())[0]
    if key=='month':
        if value>12:
            LoggingMixin().log.warning(f"InvalidFormat: Months must between 1..12")
            bool=False
    elif key=='day':
        if value>31:
            LoggingMixin().log.warning(f"InvalidFormat: Days must between 1..31")
            bool=False
    return bool


def dates(number,args=None):
    """
        Generator function for dates
        :param number: Number of records to generate
        :type int
        :param args: schema attribute values
        :type dict
        :return: list
    """
    date_list=[]
    start_day = start_month = start_year = 0
    end_day = end_month = end_year = 0

    if args is not None:
        format=args.get('format','dd/mm/YYYY')
        start=args.get('start','10/10/2019')
        end=args.get('end','10/10/2020')
        if get_seperator(format) != get_seperator(start) or get_seperator(format) != get_seperator(end)  \
                or get_seperator(start) != get_seperator(end):
            format = 'dd/mm/YYYY'
            start = '10/10/2019'
            end = '10/10/2020'
            LoggingMixin().log.warning(f"InvalidFormat: date format mismatch")
    else:
        format ='dd/mm/YYYY'
        start = '10/10/2019'
        end = '10/10/2020'

    strftime_list=list(map(lambda x: x[0] if len(x)>1 else x , split(format)))
    strftime=get_seperator(format).join(list(map(lambda x: '%'+x,strftime_list)))

    for f,s,e in zip(split(format), split(start), split(end)):
        if f=='mm':
            start_month=int(s)
            end_month=int(e)
            start_month= start_month if validate({'month':start_month}) else 10
            end_month = start_month if validate({'month': end_month}) else 10
        if f=='dd':
            start_day=int(s)
            end_day=int(e)
            start_day = start_day if validate({'day': start_day}) else 10
            end_day = end_day if validate({'day': end_day}) else 10
        if 'y' in f or 'Y' in f:
            start_year=int(s)
            end_year=int(e)

        for _  in range(number):
            if start_year>0:
                fake = Faker()
                start = datetime.date(year=start_year, month=start_month, day=start_day)
                end = datetime.date(year=end_year, month=end_month, day=end_day)
                date= str(fake.date_between(start_date=start, end_date=end).strftime(strftime))
                date_list.append(date)
    return  date_list


def day(number):
    """
     Generator function for days
     :param number: Number of records to generate
     :type int
     :return: list
     """
    faker = Faker()
    return [faker.date_between().strftime('%a') for _ in range(number)]


def month(number):
    """
     Generator function for months
     :param number: Number of records to generate
     :type int
     :return: list
     """
    faker = Faker()
    return [faker.date_between().strftime('%B') for _ in range(number)]

def time(number):
    """
     Generator function for words
     :param number: Number of records to generate
     :type int
     :return: list
     """
    faker = Faker()
    return [faker.time() for _ in range(number)]

def timestamp(number):
    """
     Generator function for timestamps
     :param number: Number of records to generate
     :type int
     :return: list
     """
    faker = Faker()
    return [str(faker.date_time_between()) for _ in range(number)]
