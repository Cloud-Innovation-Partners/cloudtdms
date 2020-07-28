#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

import pandas as pd
import random
import os
from faker import Faker
from faker.providers import person
from airflow.utils.log.logging_mixin import LoggingMixin

# {'univ-$-university': {}, 'lang-$-gender': {}, 'sex-$-gender': {}, 'first_name-$-first_name': {}, 'email-$-email_address': {}}
def personal(data_frame, number, args):
    field_names = {}
    for k in args:
        if k.split('-$-',2)[1] not in field_names:
            field_names[k.split('-$-',2)[1]] = {k.split('-$-',2)[0]: args.get(k)}
        else:
            field_names[k.split('-$-',2)[1]][k.split('-$-',2)[0]] = args.get(k)

    columns = field_names.keys()
    # Set locale
    locale = 'en_GB'
    for e in args.values():
        l = e.get('locale')
        if l is not None:
            if os.path.exists(f"{os.path.dirname(__file__)}/{l}"):
                locale = e.get('locale')
            else:
               LoggingMixin().log.error(f"InvalidValue found for attribute `locale` in schema.")
               locale = 'en_GB'
            break

    df = pd.read_csv(f"{os.path.dirname(__file__)}/{locale}/person.csv")

    # {'university': {'univ2': {}}, 'language': {'lang': {}}, 'gender': {'sex': {'set_val': 'M,F'}}, 'first_name': {'first_name': {'category': 'male'}}}
    # gender
    gender = None
    if 'first_name' in field_names:
        first_name_columns = field_names.get('first_name')
        first_name_attribs = list(first_name_columns)
        for attrib in first_name_attribs:
            if 'category' in first_name_columns.get(attrib):
                gender = first_name_columns.get(attrib).get('category')
                break

    elif 'full_name' in field_names:
        full_name_columns = field_names.get('full_name')
        full_name_attribs = list(full_name_columns)
        for attrib in full_name_attribs:
            if 'category' in full_name_columns.get(attrib):
                gender = full_name_columns.get(attrib).get('category')
                break
    else:
        gender = None

    if gender is not None:
        gender = 'Male' if str(gender).startswith('m') else 'Female'
        sex = pd.Series(gender)
        mask = df['gender'].isin(sex)
        df = df[mask]

    title = {'Male': ['Mr', 'Dr', 'Honorable', 'Rev'], 'Female': ['Ms', 'Mrs', 'Honorable', 'Dr']}

    if 't_first_name' in df.columns and 't_last_name' in df.columns:
        # first_name
        tf_data_frame = pd.DataFrame(tuple(df[['first_name', 't_first_name','gender']].iloc[random.randint(0,len(df)-1)] for _ in range(number)))
        tf_data_frame.reset_index(drop=True,inplace=True)
        data_frame[['first_name', 't_first_name', 'gender']] = tf_data_frame
        # last_name
        tl_data_frame = pd.DataFrame(tuple(df[['last_name','t_last_name']].iloc[random.randint(0,len(df)-1)] for _ in range(number)))
        tl_data_frame.reset_index(drop=True, inplace=True)
        data_frame[['last_name', 't_last_name']] = tl_data_frame
    else:
        # first_name
        tf_data_frame = pd.DataFrame(tuple(df[['first_name', 'gender']].iloc[random.randint(0, len(df)-1)] for _ in range(number)))
        tf_data_frame.reset_index(drop=True, inplace=True)
        data_frame[['first_name', 'gender']] = tf_data_frame
        # last_name
        tl_data_frame = pd.Series([df['last_name'].iloc[random.randint(0, len(df)-1)] for _ in range(number)])
        tl_data_frame.reset_index(drop=True, inplace=True)
        data_frame['last_name'] = tl_data_frame

    # full_name
    data_frame['full_name'] = data_frame['first_name'] + " " + data_frame['last_name']
    # email
    if 't_first_name' not in data_frame.columns and 't_last_name' not in data_frame.columns:
        data_frame['email_address'] = data_frame['first_name'].str.lower().astype(str).str[0]+ pd.Series([random.choice(['.', '_', '']) for _ in range(number)])+data_frame['last_name'].apply(lambda x : str(x).lower().strip().replace(' ','_'))+pd.Series([str(random.randint(10,999)) for _ in range(number)])+'@'+pd.Series([random.choice(['gmail.com','yahoo.com','mail.com','ymail.com','outlook.com','yandex.com','rediffmail.com','zoho.com']) for _ in range(number)])
    else:
        data_frame['email_address'] = data_frame['t_first_name'].str.lower().astype(str).str[0]+ pd.Series([random.choice(['.', '_', '']) for _ in range(number)])+data_frame['t_last_name'].apply(lambda x : str(x).lower().strip().replace(' ','_'))+pd.Series([str(random.randint(10,999)) for _ in range(number)])+'@'+pd.Series([random.choice(['gmail.com','yahoo.com','mail.com','ymail.com','outlook.com','yandex.com','rediffmail.com','zoho.com']) for _ in range(number)])

    # username
    if 't_first_name' not in data_frame.columns and 't_last_name' not in data_frame.columns:
        data_frame['username'] = data_frame['first_name'].str.lower().astype(str).str[:3]+pd.Series([random.choice(['', '_']) for _ in range(number)])+data_frame['last_name'].apply(lambda x : str(x).lower().strip().replace(' ','_'))+pd.Series([str(random.randint(1,999)) for _ in range(number)])
    else:
        data_frame['username'] = data_frame['t_first_name'].str.lower().astype(str).str[:3]+pd.Series([random.choice(['', '_']) for _ in range(number)])+data_frame['t_last_name'].apply(lambda x : str(x).lower().strip().replace(' ','_'))+pd.Series([str(random.randint(1,999)) for _ in range(number)])
    # title
    func = lambda x: random.choice(title['Male']) if x == 'Male' else random.choice(title['Female'])
    data_frame['title'] = data_frame['gender'].apply(func)

    if 'university' in columns:
        if os.path.exists(f"{os.path.dirname(__file__)}/{locale}/university.csv"):
            univ = pd.read_csv(f'{os.path.dirname(__file__)}/{locale}/university.csv', usecols=['university'])
        else:
            univ = pd.read_csv(f'{os.path.dirname(__file__)}/university.csv', usecols=['university'])
        data_frame['university'] = pd.Series([univ.iloc[random.randint(0, len(univ)-1)]['university'] for _ in range(number)])
    if 'language' in columns:
        fake = Faker()
        fake.add_provider(person)
        data_frame['language'] = pd.Series([fake.language_name() for _ in range(number)])

    for col in ['first_name', 'last_name', 'full_name', 'email_address', 'gender', 'title', 'username']:
        if col not in columns:
            data_frame.drop(col, inplace=True, axis=1)

    #Remove translated columns if any
    if 't_first_name' in data_frame.columns:
        data_frame.drop('t_first_name', inplace=True, axis=1)
    if 't_last_name' in data_frame.columns:
        data_frame.drop('t_last_name', inplace=True, axis=1)

    #{'gender': {'lang': {'category': 'male'}, 'sex': {'category': 'female'}}, 'first_name': {'fname1': {}, 'fname2':{}}, 'email_address': {'email': {}}, 'university': {'univ': {}}, 'language': {'lang': {}}}
    for item in field_names:
        count = len(field_names[item])
        column_names = list(field_names[item].keys())
        if count > 0:
            data_frame.rename(columns={item:column_names[0]}, inplace=True)
            for i in range(1,len(column_names)):
                data_frame[f"{item}{i}"] = data_frame[column_names[0]]
                data_frame.rename(columns={f"{item}{i}" : column_names[i]}, inplace=True)
                random.shuffle(data_frame[column_names[i]])


def first_name(number, args=None):
    raise NotImplemented


def last_name(number, args=None):
    raise NotImplemented


def full_name(number, args=None):
    raise NotImplemented


def gender(number, args=None):
    raise NotImplemented


def username(number, args=None):
    raise NotImplemented


def email_address(number, args=None):
    raise NotImplemented


def language(number, args=None):
    raise NotImplemented


def university(number, args=None):
    raise NotImplemented


def title(number, args=None):
    raise NotImplemented