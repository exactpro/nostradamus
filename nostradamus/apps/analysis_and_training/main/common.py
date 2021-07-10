from typing import Union

from pandas import DataFrame, Series
from utils.const import STOP_WORDS
from itertools import chain

MIN_CLASS_PERCENTAGE = 0.01


def check_bugs_count(issues: DataFrame, required_count: int = 100) -> bool:
    """Checks the number of bugs in the dataset.

    Parameters:
    ----------
    issues:
        Bug reports.
    required_count:
        required count bugs.

    Returns:
    ----------
        True, if the required count of bugs is present in the dataset,
        otherwise it is False.
    """
    return len(issues.index) >= required_count


def unpack_lists(lists: list) -> list:
    """Unpacks two-dimensional lists to one-dimensional.

    Parameters:
    ----------
    lists:
        two-dimensional list.

    Returns:
    ----------
        Unpacked one-dimensional list.
    """
    return list(chain(*lists))


def check_required_percentage(series: Series, value: Union[str, int]) -> bool:
    """Checks whether the value represents required percentage
    in handled series.

    Parameters:
    ----------
    series:
        series used for percentage calculations.
    value:
        metric is used for percentage calculations.

    Returns:
    ----------
        True if value percentage is greater than 1% from the whole series
        otherwise False.
    """
    return series[series == value].size / series.size >= MIN_CLASS_PERCENTAGE


def get_assignee_reporter(issues: DataFrame) -> set:
    """Parsing full names from Assignee and Reported series

    Parameters:
    ----------
    issues:
        Bug reports.

    Returns:
    ----------
        Unique names and last names.
    """
    full_names = [
        full_name.lower().split()
        for full_name in issues["Assignee"].tolist()
        + issues["Reporter"].tolist()
    ]

    assignee_reporter = set(unpack_lists(full_names))

    return assignee_reporter


def get_stop_words(issues: DataFrame) -> set:
    """Generates stop words for TfidfVectorizer constructor.

    Parameters:
    ----------
    issues:
        Bug reports.

    Returns:
    ----------
        Unique words which will be ignored.
    """
    assignee_reporter = get_assignee_reporter(issues)

    return STOP_WORDS.union(assignee_reporter)
