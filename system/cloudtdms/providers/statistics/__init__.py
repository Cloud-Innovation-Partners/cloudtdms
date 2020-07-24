#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from airflow import LoggingMixin
import numpy as np


def statistics(data_frame, number, args):
    field_names = {}
    for k in args:
        if k.split('-$-', 2)[1] not in field_names:
            field_names[k.split('-$-', 2)[1]] = {k.split('-$-', 2)[0]: args.get(k)}
        else:
            field_names[k.split('-$-', 2)[1]][k.split('-$-', 2)[0]] = args.get(k)

    columns = field_names.keys()

    for col in columns:
        mod = globals()[col]
        mod(data_frame, number, field_names.get(col))


def poisson(data_frame, number,args=None):
    """
    Generator function for poisson
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("poisson")]
    for column_name, data_frame_col_name in zip(args, dcols):
        mean= args.get(column_name).get('mean',0) if args is not None else 0
        if mean < 0:
            LoggingMixin().log.warning(f"InvalidValue: poisson set_value must be greater than zero")
            mean=0
        data_frame[data_frame_col_name] = np.random.poisson(mean,number)
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def normal(data_frame, number,args=None):
    """
    Generator function for normal
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("normal")]
    for column_name, data_frame_col_name in zip(args, dcols):
        center= args.get(column_name).get('center',0) if args is not None else 0
        std_dev = args.get(column_name).get('std_dev', 1) if args is not None else 1
        decimals = args.get(column_name).get('decimals', 8) if args is not None else 8

        if decimals>8:
            LoggingMixin().log.warning(f"InvalidValue: decimals value must be less than 9")
            decimals = 8

        if center < 0:
            LoggingMixin().log.warning(f"InvalidValue: center must be greater than zero")
            center=1

        if std_dev < 0:
            LoggingMixin().log.warning(f"InvalidValue: std_dev must be greater than zero")
            std_dev=1

        normal_list=np.random.normal(loc=center, scale=std_dev, size=number)
        normal_list= [f"%.{decimals}f"%item for item in normal_list]
        data_frame[data_frame_col_name] = normal_list
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def binomial(data_frame, number,args=None):
    """
    Generator function for binomial
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("binomial")]
    for column_name, data_frame_col_name in zip(args, dcols):
        success_rate= args.get('success_rate',0.5) if args is not None else 0.5

        if success_rate >1 or success_rate < 0:
            LoggingMixin().log.warning(f"InvalidValue:success_rate must between 0 and 1")
            success_rate=0.5

        data_frame[data_frame_col_name] = np.random.binomial(n=1, p=success_rate, size=number)
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def exponential(data_frame, number,args=None):
    """
    Generator function for exponential
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("exponential")]
    for column_name, data_frame_col_name in zip(args, dcols):
        _scale= args.get(column_name).get('scale',5) if args is not None else 5

        if _scale < -1:
            LoggingMixin().log.warning(f"InvalidValue: scale must be greater than 0")
            _scale=1

        exp_list=np.random.exponential(scale=_scale, size=number)
        exp_list = ["%.9f" % item for item in exp_list]
        data_frame[data_frame_col_name] = sorted(exp_list)
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)


def geometric(data_frame, number,args=None):
    """
    Generator function for geometric
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    dcols = [f for f in data_frame.columns if f.startswith("geometric")]
    for column_name, data_frame_col_name in zip(args, dcols):
        success_rate= args.get(column_name).get('success_rate',0.5) if args is not None else 0.5

        if success_rate >1 or success_rate < 0:
            LoggingMixin().log.warning(f"InvalidValue:success_rate must between 0 and 1")
            success_rate=0.5

        data_frame[data_frame_col_name] = np.random.geometric( p=success_rate, size=number)
        data_frame.rename(columns={data_frame_col_name: column_name}, inplace=True)
