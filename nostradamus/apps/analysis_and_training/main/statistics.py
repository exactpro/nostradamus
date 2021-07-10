import numpy as np
import pandas as pd

from utils.data_converter import math_round


def calculate_statistics(issues: pd.DataFrame, series: list) -> dict:
    """Calculates the following metrics for handled series:
        - minimum value;
        - maximum value;
        - mean value;
        - standard deviation (std).

    :param issues: DataFrame to be used for calculations.
    :param series: Series names to be used as metrics for calculations.
    :return: Calculated statistics.
    """
    statistics = {}
    for name in series:
        try:
            if name == "Time to Resolve":
                issues = issues[issues.Resolution != "Unresolved"]
            compute = {
                "max": str(issues[name].max()),
                "min": str(issues[name].min()),
                "mean": str(int(math_round(issues[name].mean()))),
                "std": str(int(math_round(np.nan_to_num(issues[name].std())))),
            }
        except (TypeError, ValueError):
            compute = {
                "max": "0",
                "min": "0",
                "mean": "0",
                "std": "0",
            }

        if name == "Time to Resolve":
            name = "Time to Resolve (TTR)"
        statistics.update({name: compute})
    return statistics
