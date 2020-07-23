#  Copyright (c) 2020. Cloud Innovation Partners (CIP)
#  CloudTDMS - Test Data Management Service

from airflow import LoggingMixin
import  numpy as np

def poisson(number,args=None):
    """
    Generator function for poisson
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    mean= args.get('mean',0) if args is not None else 0
    if mean < 0:
        LoggingMixin().log.warning(f"InvalidValue: poisson set_value must be greater than zero")
        mean=0
    return np.random.poisson(mean,number)


def normal(number,args=None):
    """
    Generator function for normal
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    center= args.get('center',0) if args is not None else 0
    std_dev = args.get('std_dev', 1) if args is not None else 1
    decimals = args.get('decimals', 8) if args is not None else 8

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
    return normal_list


def binomial(number,args=None):
    """
    Generator function for binomial
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    success_rate= args.get('success_rate',0.5) if args is not None else 0.5

    if success_rate >1 or success_rate < 0:
        LoggingMixin().log.warning(f"InvalidValue:success_rate must between 0 and 1")
        success_rate=0.5

    return np.random.binomial(n=1, p=success_rate, size=number)


def exponential(number,args=None):
    """
    Generator function for exponential
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    _scale= args.get('scale',5) if args is not None else 5

    if _scale < -1:
        LoggingMixin().log.warning(f"InvalidValue: scale must be greater than 0")
        _scale=1

    exp_list=np.random.exponential(scale=_scale, size=number)
    exp_list = ["%.9f" % item for item in exp_list]
    return sorted(exp_list)

def geometric(number,args=None):
    """
    Generator function for geometric
    :param number: Number of records to generate
    :type int
    :param args: schema attribute values
    :type dict
    :return: list
    """
    success_rate= args.get('success_rate',0.5) if args is not None else 0.5

    if success_rate >1 or success_rate < 0:
        LoggingMixin().log.warning(f"InvalidValue:success_rate must between 0 and 1")
        success_rate=0.5

    return np.random.geometric( p=success_rate, size=number)
