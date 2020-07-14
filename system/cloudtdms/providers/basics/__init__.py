#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import random
import string
import os
import uuid

from airflow import LoggingMixin
from faker import Faker


def boolean(number, args=None):
    """
    Generator function for boolean values
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    if args is not None:
        value = args.get('set_val', '1,0')
        value = value if isinstance(value, str) else '1,0'
        boolean_values = value.split(',')[:2]
    else:
        boolean_values = ['true', 'false']

    boolean_weights = [0.5, 0.5]
    boolean_list = random.choices(population=boolean_values, weights=boolean_weights, k=number)
    return boolean_list


def frequency(number):
    """
    Generator function for frequency values
    :param number: Number of records to generate
    :type int
    :return: list
    """
    frequency_values = ['Never', 'Seldom', 'Once', 'Often', 'Daily', 'Weekly', 'Monthly', 'Yearly']
    frequency_list = random.choices(population=frequency_values, k=number)
    return frequency_list


def color(number, args=None):
    """
    Generator function for color values
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    source = list(string.hexdigits)

    if args is not None:
        format = args.get('format', 'hex-code')
        format = format if isinstance(format,str) else 'hex-code'
    else:
        format = 'hex-code'

    if format == 'hex-code':
        return [('#' + ''.join(source[:6]), random.shuffle(source))[0] for _ in range(number)]
    elif format == 'name':
        f = Faker()
        return [f.color_name() for _ in range(number)]
    elif format == 'short-hex':
        return [('#' + ''.join(source[:3]), random.shuffle(source))[0] for _ in range(number)]
    else:
        LoggingMixin().log.warning(f"InvalidAttribute: Invalid `format` = {format} value found!")
        return [('#' + ''.join(source[:6]), random.shuffle(source))[0] for _ in range(number)]


def words(number, args=None):
    """
    Generator function for words
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    words_list = []
    if args is not None:
        atleast = int(args.get('atleast', 1))
        atmost = int(args.get('atmost', 3))
        if atleast == 1:
            LoggingMixin().log.warning(f"InvalidAttribute: Invalid name for `atleast`")
        if atmost == 3:
            LoggingMixin().log.warning(f"InvalidAttribute: Invalid name for `atmost`")
    else:
        atleast = 1
        atmost = 3

    path = os.path.dirname(__file__)+"/words.txt"
    print(path)
    words = open(path).read().splitlines()
    for _ in range(number):
        how_many = random.randint(atleast, atmost)
        random.shuffle(words)
        words_list.append(' '.join(words[:how_many]))
    return words_list


def sentence(number, args=None):
    """
    Generator function for sentences
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """

    sentence_list = []
    if args is not None:
        atleast = int(args.get('atleast', 1))
        atmost = int(args.get('atmost', 3))
        if atleast == 1:
            LoggingMixin().log.warning(f"InvalidAttribute: Invalid name for `atleast`")
        if atmost == 3:
            LoggingMixin().log.warning(f"InvalidAttribute: Invalid name for `atmost`")
    else:
        atleast = 1
        atmost = 3
    path = os.path.dirname(__file__)+"/words.txt"
    words = open(path).read().splitlines()
    for _ in range(number):
        random.shuffle(words)
        how_many = random.randint(atleast, atmost)
        sentence = [(' '.join(words[:4]) + ". ", random.shuffle(words)) for _ in range(how_many)]
        sentence = list(map(lambda x: x[0][0].upper() + x[0][1:], sentence))
        sentence_list.append(' '.join(sentence))
    return sentence_list

print(sentence(10))

def blank(number):
    return [None] * number


def UUID(number):
    return [str(uuid.uuid4()) for _ in range(number)]


def password(number, args=None):
    passwords = []
    if args is not None:
        length = int(args.get('length',8))
        if length == 8:
            LoggingMixin().log.warning(f"InvalidAttribute: Invalid name for `password`")
    else:
        length = 8
    source = list(string.ascii_letters + string.digits)

    for _ in range(number):
        random.shuffle(source)
        password = ''.join(source[:length])
        passwords.append(password)

    return passwords


def auto_increment(number, args=None):
    if args is not None:
        start = int(args.get('start', 0))
        inc = int(args.get('inc', 1))
        prefix = args.get('prefix', '')
        suffix = args.get('suffix', '')
        # if start == 0:
        #     LoggingMixin().log.warning(f"InvalidAttribute: Invalid name for `start`")
        # if inc == 1:
        #     LoggingMixin().log.warning(f"InvalidAttribute: Invalid name for `inc`")
        # if len(prefix) == 0:
        #     LoggingMixin().log.warning(f"InvalidAttribute: Invalid name for `prefix`")
        # if len(suffix) == 0:
        #     LoggingMixin().log.warning(f"InvalidAttribute: Invalid name for `suffix`")

    else:
        start = 0
        inc = 1
        prefix = ''
        suffix = ''

    range_list = list(range(start, start + number, inc))
    range_list_len = len(range_list)
    if range_list_len < number:
        diff = number - range_list_len
        last_elem = range_list[-1]
        extra_elems = [last_elem] * diff
        extra_elems = extra_elems[:number]
        range_list.extend(extra_elems)

    range_list = [prefix + str(i) + suffix if len(prefix) > 0 or len(suffix) > 0 else i for i in range_list]
    return range_list


def random_number(number, args=None):
    start = end = 0
    if args is not None:
        start = int(args.get('start',0))
        end = int(args.get('end',300))
    else:
        start = 0
        end = 300

    random_range_list = []
    for _ in range(number):
        random_range_list.append(random.randint(start, end))
    return random_range_list


def number_range(number, args=None):
    if args is not None:
        start = int(args.get('start', 0))
        end = int(args.get('end', 20))
    else:
        start = 0
        end = 20

    range_list = list(range(start, end + 1))
    range_list_len = len(range_list)
    if range_list_len < number:
        diff = number - range_list_len
        range_list = range_list * diff
        range_list = range_list[:number]

    return range_list
