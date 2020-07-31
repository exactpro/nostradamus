import pandas as pd

from utils.const import PERIOD_MAPPING, PERIOD_FORMAT_MAPPING


def get_defect_submission(df: pd.DataFrame, period: str) -> dict:
    """ Calculates coordinates for defect submission chart.

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
    chart_period = PERIOD_MAPPING[period]
    date_format = PERIOD_FORMAT_MAPPING[period]

    df.set_index(df["Created"], inplace=True)
    coordinates = df["Key"].resample(chart_period).count().cumsum()
    coordinates.index = coordinates.index.strftime(date_format)
    coordinates = coordinates.to_dict()

    return coordinates
