#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import random


def custom_list(number, args=None):
    """
    Generator function for custom_list
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    set_val = args.get('set_val', "") if args is not None else ""

    return list([random.choice(set_val.split(',')) for _ in range(int(number))])

