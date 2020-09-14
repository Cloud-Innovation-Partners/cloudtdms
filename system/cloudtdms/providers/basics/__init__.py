#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import random
import string
import os
import uuid
import math

from airflow import LoggingMixin
from faker import Faker

def basics(data_frame, number, args):
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
        if col == 'boolean':
            boolean(data_frame, number, field_names.get('boolean'))

        if col == 'frequency':
            frequency(data_frame, number, field_names.get('frequency'))

        if col == 'color':
            color(data_frame, number, field_names.get('color'))

        if col == 'words':
            words(data_frame, number, field_names.get('words'))

        if col == 'sentence':
            sentence(data_frame, number, field_names.get('sentence'))

        if col == 'blank':
            blank(data_frame, number,field_names.get('blank'))

        if col == 'guid':
            guid(data_frame, number,field_names.get('guid'))

        if col == 'password':
            password(data_frame, number, field_names.get('password'))

        if col == 'auto_increment':
            auto_increment(data_frame, number, field_names.get('auto_increment'))

        if col == 'random_number':
            random_number(data_frame, number, field_names.get('random_number'))

        if col == 'number_range':
            number_range(data_frame, number, field_names.get('number_range'))

def boolean(data_frame, number, args=None):
    """
    Generator function for boolean values
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("boolean")]
    for column_name, data_frame_col_name in zip(args, dcols):
        if args is not None:
            value = args.get(column_name).get('set_val', '1,0')
            value = value if isinstance(value, str) else '1,0'
            boolean_values = value.split(',')[:2]
        else:
            boolean_values = ['1', '0']

        boolean_weights = [0.5, 0.5]
        boolean_list = random.choices(population=boolean_values, weights=boolean_weights, k=number)
        data_frame[data_frame_col_name]= boolean_list
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def frequency(data_frame, number, args=None):
    """
    Generator function for frequency values
    :param number: Number of records to generate
    :type int
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("frequency")]
    for column_name, data_frame_col_name in zip(args, dcols):
        frequency_values = ['Never', 'Seldom', 'Once', 'Often', 'Daily', 'Weekly', 'Monthly', 'Yearly']
        frequency_list = random.choices(population=frequency_values, k=number)
        data_frame[data_frame_col_name]=frequency_list

        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)



def color(data_frame, number, args=None):
    """
    Generator function for color values
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    source = list(string.hexdigits)
    dcols = [f for f in data_frame.columns if f.startswith("color")]
    for column_name, data_frame_col_name in zip(args, dcols):

        if args is not None:
            format = args.get(column_name).get('format', 'hex-code')
            format = format if isinstance(format,str) else 'hex-code'
        else:
            format = 'hex-code'

        if format == 'hex-code':
            data_frame[data_frame_col_name] = [('#' + ''.join(source[:6]), random.shuffle(source))[0] for _ in range(number)]
        elif format == 'name':
            f = Faker()
            data_frame[data_frame_col_name] = [f.color_name() for _ in range(number)]
        elif format == 'short-hex':
            data_frame[data_frame_col_name] = [('#' + ''.join(source[:3]), random.shuffle(source))[0] for _ in range(number)]
        else:
            LoggingMixin().log.warning(f"InvalidAttribute: Invalid `format` = {format} value found!")
            data_frame[data_frame_col_name] = [('#' + ''.join(source[:6]), random.shuffle(source))[0] for _ in range(number)]

        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)

def words(data_frame, number, args=None):
    """
    Generator function for words
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    words_list = []
    dcols = [f for f in data_frame.columns if f.startswith("words")]
    for column_name, data_frame_col_name in zip(args, dcols):
        if args is not None:
            atleast = int(args.get(column_name).get('atleast', 1))
            atmost = int(args.get(column_name).get('atmost', 3))
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
            how_many = random.randint(atleast, atmost)
            random.shuffle(words)
            words_list.append(' '.join(words[:how_many]))
        data_frame[data_frame_col_name] = words_list
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)

def sentence(data_frame, number, args=None):
    """
    Generator function for sentences
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """

    sentence_list = []
    dcols = [f for f in data_frame.columns if f.startswith("sentence")]
    for column_name, data_frame_col_name in zip(args, dcols):
        if args is not None:
            atleast = int(args.get(column_name).get('atleast', 1))
            atmost = int(args.get(column_name).get('atmost', 3))
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
        data_frame[data_frame_col_name] = sentence_list
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)

def blank(data_frame, number, args=None):
    """
      Generator function for Null values
      :param number: Number of records to generate
      :type int
      :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("blank")]
    for column_name, data_frame_col_name in zip(args, dcols):
        data_frame[data_frame_col_name]=  [None] * number
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def guid(data_frame, number, args=None):
    """
      Generator function for UUID values
      :param number: Number of records to generate
      :type int
      :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("blank")]
    for column_name, data_frame_col_name in zip(args, dcols):
        data_frame[data_frame_col_name] = [str(uuid.uuid4()) for _ in range(number)]
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)

def password(data_frame, number, args=None):
    """
       Generator function for passwords
       :param number: Number of records to generate
       :type int
       :param args: schema attribute values
       :type dict
       :return: list
    """
    passwords = []
    dcols = [f for f in data_frame.columns if f.startswith("password")]
    for column_name, data_frame_col_name in zip(args, dcols):
        if args is not None:
            length = int(args.get(column_name).get('length',8))
            if length == 8:
                LoggingMixin().log.warning(f"InvalidAttribute: Invalid name for `password`")
        else:
            length = 8
        source = list(string.ascii_letters + string.digits)

        for _ in range(number):
            random.shuffle(source)
            password = ''.join(source[:length])
            passwords.append(password)

        data_frame[data_frame_col_name] =passwords
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)

def auto_increment(data_frame, number, args=None):
    """
       Generator function for auto increment
       :param number: Number of records to generate
       :type int
       :param args: schema attribute values
       :type dict
       :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("auto_increment")]
    for column_name, data_frame_col_name in zip(args, dcols):

        if args is not None:
            start = int(args.get(column_name).get('start', 0))
            inc = int(args.get(column_name).get('increment', 1))
            prefix = args.get(column_name).get('prefix', '')
            suffix = args.get(column_name).get('suffix', '')
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
        data_frame[data_frame_col_name]= range_list
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)

def random_number(data_frame, number, args=None):
    """
       Generator function for random numbers
       :param number: Number of records to generate
       :type int
       :param args: schema attribute values
       :type dict
       :return: list
    """
    start = end = 0
    dcols = [f for f in data_frame.columns if f.startswith("random_number")]
    for column_name, data_frame_col_name in zip(args, dcols):
        if args is not None:
            start = int(args.get(column_name).get('start',0))
            end = int(args.get(column_name).get('end',300))
        else:
            start = 0
            end = 300

        random_range_list = []
        for _ in range(number):
            random_range_list.append(random.randint(start, end))
        data_frame[data_frame_col_name]= random_range_list
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def number_range(data_frame, number, args=None):
    """
       Generator function for number range
       :param number: Number of records to generate
       :type int
       :param args: schema attribute values
       :type dict
       :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("number_range")]
    for column_name, data_frame_col_name in zip(args, dcols):

        if args is not None:
            start = int(args.get(column_name).get('start', 0))
            end = int(args.get(column_name).get('end', 20))
        else:
            start = 0
            end = 20

        range_list = list(range(start, end + 1))
        range_list_len = len(range_list)
        if range_list_len < number:
            diff = number - range_list_len
            diff = math.ceil(number / diff)
            range_list += range_list * diff
            range_list = range_list[:number]
        elif range_list_len > number:
            range_list = range_list[:number]

        data_frame[data_frame_col_name] = range_list
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)
