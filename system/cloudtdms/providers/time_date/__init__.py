#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from faker import Faker
from datetime import  datetime
import random

def date(number, args=None):
    dates=[]
    faker=Faker()

    if args is not None:
        start_date=args.get('start_date')
        end_date=args.get('end_date')
    else:
        start_date = 'today'
        end_date ='+30y'

    for _ in range(number):
        date=faker.date_between(start_date=start_date, end_date=end_date)
        date=date.strftime('%m/%d/%Y')
        dates.append(date)

    return dates

def day(number):
    faker = Faker()
    return [faker.date_between().strftime('%a') for _ in range(number)]

def month(number):
    faker = Faker()
    return [faker.date_between().strftime('%B') for _ in range(number)]

def time(number):
    faker = Faker()
    return [faker.time() for _ in range(number)]

def timestamp(number):
    faker = Faker()
    return [faker.date_time_between() for _ in range(number)]
