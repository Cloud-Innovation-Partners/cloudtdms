#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import random
import string
import os
import uuid



def boolean(number,args):
    """
    :param number:
    :type int
    :param args:
    :type dict
    :return:
    """
    boolean_values=args.get('list')
    boolean_weights=args.get('weights')

    if boolean_weights is  None:
        boolean_weights=[0.5,0.5]

    boolean_list = random.choices(population=boolean_values, weights=boolean_weights, k=number)
    return boolean_list

def frequency(number,args):
    frequency_values=args['list']
    frequency_list = random.choices(population=frequency_values, k=number)
    return frequency_list

def color(number):
    colors = []
    source = list(string.hexdigits)

    for _ in range(number):
        random.shuffle(source)
        random.shuffle(source)
        color = '#' + ''.join(source[:6])
        colors.append(color)

    return colors

def words(number):
    path = os.path.dirname(__file__).replace('basics', 'words.txt')
    words = open(path).read().splitlines()
    random.shuffle(words)
    return words[:number]

def sentence(number,args=None):
    senteance_list=[]
    if args is not None:
        min_length = args.get('min_length')
    else:
        min_length=8
    path = os.path.dirname(__file__).replace('basics', 'words.txt')
    words = open(path).read().splitlines()
    for _ in range(number):
        random.shuffle(words)
        senteance_list.append(' '.join(words[:min_length]))

    return senteance_list

def blank(number):
    return [None]*number

def UUID(number):
    return [ str(uuid.uuid4()) for _ in range(number)]

def password(number,args=None):
    passwords=[]
    if args is not None:
        min_length = args.get('min_length')
    else:
        min_length = 8
    source = list(string.ascii_letters + string.digits)

    for _ in range(number):
        random.shuffle(source)
        password = ''.join(source[:min_length])
        passwords.append(password)

    return passwords

def auto_increment(number):
    return range(number)


def number_range(number,args=None):
    start=end=inc=0
    if args is not None:
        start=args['start']
        end=args['end']
        inc=args['inc']
    else:
        start = 0
        end = 1000
        inc = 2

    range_list=list(range(start,end,inc))
    range_list_len=len(range_list)
    if range_list_len<number:
        diff=number-range_list_len
        last_elem=range_list[-1]
        last_elem=range_list[-1]
        extra_elems=[last_elem]*diff
        extra_elems=extra_elems[:number]
        range_list.extend(extra_elems)
    return range_list

def random_range(number,args=None):
    start = end = 0
    if args is not None:
        start = args['start']
        end = args['end']
    else:
        start = 0
        end = 300

    random_range_list=[]
    for _ in range(number):
        random_range_list.append(random.randint(start,end))
    return random_range_list



