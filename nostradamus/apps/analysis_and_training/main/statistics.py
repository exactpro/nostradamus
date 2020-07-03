import numpy as np
import pandas as pd

from utils.data_converter import math_round


def calculate_statistics(df: pd.DataFrame, series: list) -> dict:
    """Calculates the following metrics for handled series:
        - minimum value;
        - maximum value;
        - mean value;
        - standard deviation (std).

    Parameters
    ----------
    df:
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
                df = df[df.Resolution != "Unresolved"]
            statistics.update(
                {
                    name: {
                        "minimum": str(df[name].min()),
                        "maximum": str(df[name].max()),
                        "mean": str(int(math_round(df[name].mean()))),
                        "std": str(
                            int(math_round(np.nan_to_num(df[name].std())))
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
