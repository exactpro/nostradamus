import math
import datetime
import pandas as pd


# TODO
# 1. this function has to be moved to a module which is related to charts logic
#    because this one is used by Defect Submission chart only
# 2. format docstring
def stringify_date(date: datetime, step_size: str):
    """Stringifies date argument value for specific period.

    Parameters:
        date: date in original format;
        step_size: step size value.

    Returns:
        date(str): stringified date value.
    """

    if date is None:
        return ""

    day = date.day
    month = date.month
    year = date.year

    if step_size == "10D" or step_size == "W-SUN":
        date = datetime.date(year, month, day).strftime("%Y-%m-%d")
        return date

    if step_size in ["3M", "6M"]:
        month = str(month)
        if len(month) == 1:
            month = "0" + month
        date = datetime.datetime.date(
            pd.to_datetime(str(year) + "-" + month)
        ).strftime("%Y-%m")
        return date

    if step_size == "A-DEC":
        return datetime.datetime.date(pd.to_datetime(str(date.year))).strftime(
            "%Y"
        )


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
    utc_date = utc_date - utc_date.utcoffset()

    return utc_date
