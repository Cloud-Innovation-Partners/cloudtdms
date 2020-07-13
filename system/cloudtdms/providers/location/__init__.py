#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from faker import Faker

def country(number):
    countries=[]
    faker=Faker()
    for _ in range(number):
        countries.append(faker.country())

    return  countries

