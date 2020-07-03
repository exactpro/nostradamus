import pandas as pd

from utils.const import PERIOD_MAPPING


def calculate_defect_submission(df: pd.DataFrame, period: str) -> dict:
    """ Calculates coordinates for Cumulative chart of defect submission.

    Parameters:
    ----------
        df:
            Bug reports.
        period:
            Time period to be used in calculations.

    Returns:
    ----------
        Chart coordinates.
    """
    df.set_index(df["Created"], inplace=True)

    chart_period = PERIOD_MAPPING[period]

    result = df["Key"].resample(chart_period).count().cumsum()
    result.index = result.index.strftime("%Y-%m-%d")

    result = dict(zip(result.index, result))

    return result
