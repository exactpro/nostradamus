from typing import List, Set

from pandas import DataFrame, Series, Interval

MIN_CLASS_PERCENTAGE = 0.01


def check_bugs_count(issues: DataFrame, required_count: int = 100) -> bool:
    """Checks the number of bugs in the dataset.

    :param issues: Bug reports.
    :param required_count: required count bugs.
    :return: True, if the required count of bugs is present in the dataset,
        otherwise it is False.
    """
    return len(issues.index) >= required_count


def check_required_percentage(series: Series, value: str) -> bool:
    """Checks whether the value represents required percentage
    in handled series.

    :param series: series used for percentage calculations.
    :param value: metric is used for percentage calculations.
    :return: True if value percentage is greater than 1% from the whole series
        otherwise False.
    """
    return series[series == value].size / series.size >= MIN_CLASS_PERCENTAGE


def compare_resolutions(
    dataframe_resolutions: Series, required_resolutions: List[str]
) -> Set[str]:
    """Checks for difference between required resolutions and those that are present in df.

    :param dataframe_resolutions: Resolutions in the dataframe.
    :param required_resolutions: Bugs resolution.
    :return: The difference between the required resolutions and those that are present in the dataframe.
    """
    resolutions = set(required_resolutions).difference(
        set(dataframe_resolutions.unique())
    )
    return resolutions


def stringify_ttr_intervals(intervals: List[Interval]) -> List[str]:
    """Stringifies list of ttr intervals.

    :param intervals: intervals.
    :return: Stringified list of intervals.
    """
    return (
        [
            str(intervals[0].left if intervals[0].left > 0 else 0)
            + "-"
            + str(intervals[0].right)
        ]
        + [
            str(intervals[el].left + 1) + "-" + str(intervals[el].right)
            for el in range(1, len(intervals) - 1)
        ]
        + [">" + str(intervals[len(intervals) - 1].left)]
    )
