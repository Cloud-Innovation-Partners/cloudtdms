#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import random
import string
import os
import uuid
from faker import Faker



def boolean(number,args=None):

    if args is not None:
        boolean_values=args.get('set_val').split('/')
    else:
        boolean_values=['true','false']

    boolean_weights = [0.5, 0.5]
    boolean_list = random.choices(population=boolean_values, weights=boolean_weights, k=number)
    return boolean_list

def frequency(number):
    frequency_values=['Never', 'Seldom', 'Once', 'Often', 'Daily', 'Weekly', 'Monthly', 'Yearly']
    frequency_list = random.choices(population=frequency_values, k=number)
    return frequency_list

def color(number, args=None):
    colors = []
    source = list(string.hexdigits)

    if args is not None:
        format=args.get('format')
    else:
        format='hex-code'

    for _ in range(number):

        if format =='hex-code':
            random.shuffle(source)
            color = '#' + ''.join(source[:6])
        elif format =='name':
            f = Faker()
            color=f.color_name()
        else: # fromat is short-hex
            random.shuffle(source)
            color = '#' + ''.join(source[:3])


        colors.append(color)

    return colors

def words(number, args=None):
    words_list=[]
    if args is not None:
        atleast=args.get('atleast',1)
        atmost=args.get('atmost',3)
    else:
        atleast = 1
        atmost = 3

    path = os.path.dirname(__file__).replace('basic', 'words.txt')
    words = open(path).read().splitlines()
    for _ in range(number):
        how_many=random.randint(atleast,atmost)
        random.shuffle(words)
        words_list.append(' '.join(words[:how_many]))
    return words_list

def sentence(number,args=None):
    sentance_list=[]
    if args is not None:
        atleast = args.get('atleast', 1)
        atmost = args.get('atmost', 3)
    else:
        atleast = 1
        atmost = 3
    path = os.path.dirname(__file__).replace('basic', 'words.txt')
    words = open(path).read().splitlines()
    for _ in range(number):
        random.shuffle(words)
        how_many = random.randint(atleast, atmost)
        sentance=[ ( ' '.join(words[:4])+". ",random.shuffle(words))  for _ in range(how_many) ]
        sentance=list(map(lambda x:x[0][0].upper()+x[0][1:] , sentance))
        sentance_list.append(' '.join(sentance))
    return sentance_list

def blank(number):
    return [None]*number

def UUID(number):
    return [ str(uuid.uuid4()) for _ in range(number)]

def password(number,args=None):
    passwords=[]
    if args is not None:
        length = args.get('length')
    else:
        length = 8
    source = list(string.ascii_letters + string.digits)

    for _ in range(number):
        random.shuffle(source)
        password = ''.join(source[:length])
        passwords.append(password)

    return passwords

def auto_increment(number,args=None):
    if args is not None:
        start=args.get('start',0)
        inc=args.get('inc',1)
        prefix=args.get('prefix','')
        suffix=args.get('suffix','')
    else:
        start=0
        inc = 1
        prefix =''
        suffix =''

    range_list=list(range(start,start+number,inc))
    range_list_len=len(range_list)
    if range_list_len<number:
        diff=number-range_list_len
        last_elem=range_list[-1]
        extra_elems=[last_elem]*diff
        extra_elems=extra_elems[:number]
        range_list.extend(extra_elems)

    range_list=[prefix+str(i)+suffix if len(prefix)>0 or len(suffix)>0 else i for i in range_list]
    print(range_list)
    return range_list

def random_number(number,args=None):
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

