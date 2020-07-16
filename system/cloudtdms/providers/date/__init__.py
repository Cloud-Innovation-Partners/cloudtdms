#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from faker import Faker
from datetime import  datetime
import random

def date(number, args=None):
    """
     Generator function for dates
     :param number: Number of records to generate
     :type int
     :param args: schema attribute values
     :type dict
     :return: list
     """
    dates=[]
    faker=Faker()

    if args is not None:
        start_date=args.get('start_date','today')
        end_date=args.get('end_date','+30y')
    else:
        start_date = 'today'
        end_date ='+30y'

    for _ in range(number):
        date=faker.date_between(start_date=start_date, end_date=end_date)
        date=date.strftime('%m/%d/%Y')
        dates.append(date)

    return dates

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
    return [faker.date_time_between() for _ in range(number)]
