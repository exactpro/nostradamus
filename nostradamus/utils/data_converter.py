import math
import datetime
from math import floor

import pandas as pd


def optimize_dtype(series: pd.Series, dtype: str,) -> pd.Series:
    """Automatically converts series to handled data type.

    Parameters
    ----------
    series:
        Series to be converted.
    dtype:
        Data type is used for conversion.

    Returns
    -------
    pd.Series:
        Optimized pandas series.
    """
    return series.astype(dtype)


def convert_date(raw_dates: pd.Series) -> pd.Series:
    """Automatically converts series containing raw dates
    to specific format.

    Parameters
    ----------
    raw_dates:
        Series to be converted.

    Returns
    -------
        Optimized pandas series.
    """
    raw_dates = pd.to_datetime(raw_dates, utc=True)
    return raw_dates


def math_round(number):
    if number - math.floor(number) < 0.5:
        return math.floor(number)
    return math.ceil(number)


def get_utc_datetime(raw_date: str) -> datetime.datetime:
    """ Сonverts string to UTC datetime object.

    Parameters
    ----------
    raw_date:
        String to be converted.

    Returns
    -------
        UTC datetime object.
    """
    utc_date = datetime.datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%f%z")
    # FIXME: Workaround to avoid dates inconsistency
    #  e.g. 0011-04-07 and 2011-04-07
    utc_date = datetime.datetime.strftime(utc_date, "%y-%m-%dT%H:%M:%S.%f%z")
    utc_date = datetime.datetime.strptime(utc_date, "%y-%m-%dT%H:%M:%S.%f%z")
    utc_date = utc_date - utc_date.utcoffset()

    return utc_date


def convert_to_integer(value: float) -> int:
    """ Сonverts probability from float to int.

    Parameters
    ----------
    value:
        Probability to be converted.

    Returns
    -------
        Probability in percentage representation.
    """
    return int(floor((value * 100) + 0.5))
