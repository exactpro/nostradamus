import numpy as np
import pandas as pd

from utils.data_converter import math_round


def calculate_statistics(issues: pd.DataFrame, series: list) -> dict:
    """Calculates the following metrics for handled series:
        - minimum value;
        - maximum value;
        - mean value;
        - standard deviation (std).

    Parameters
    ----------
    issues:
        DataFrame to be used for calculations.
    series:
        Series names to be used as metrics for calculations.

    Returns
    -------
        Calculated statistics.
    """
    statistics = {}
    for name in series:
        try:
            if name == "Time to Resolve":
                issues = issues[issues.Resolution != "Unresolved"]
            statistics.update(
                {
                    name: {
                        "minimum": str(issues[name].min()),
                        "maximum": str(issues[name].max()),
                        "mean": str(int(math_round(issues[name].mean()))),
                        "std": str(
                            int(math_round(np.nan_to_num(issues[name].std())))
                        ),
                    }
                }
            )
        except (TypeError, ValueError):
            statistics.update(
                {
                    name: {
                        "minimum": "0",
                        "maximum": "0",
                        "mean": "0",
                        "std": "0",
                    }
                }
            )
    return statistics
