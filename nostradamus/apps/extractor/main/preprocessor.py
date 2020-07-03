import pandas as pd

from datetime import datetime as dt
from multiprocessing import Pool
from pytz import utc

from apps.extractor.main.cleaner import clean_text
from utils.const import bug_attributes, dtype_conversions
from utils.data_converter import optimize_dtype


def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """Basic DataFrame preprocessing:
        - datatypes optimization;
        - text cleaning.

    Parameters
    ----------
    df:
        Pandas DataFrame to be processed.

    Returns
    -------
    pd.DataFrame:
        Preprocessed DataFrame.
    """
    built_in_dtypes = bug_attributes.get("built-in")
    raw_dtypes = bug_attributes.get("raw")

    for col in df.columns:
        if built_in_dtypes.get(col):
            df[col] = optimize_dtype(
                df[col], dtype_conversions.get(built_in_dtypes.get(col))
            )
        elif raw_dtypes.get(col):
            df[col] = dtype_conversions.get(raw_dtypes.get(col))(df[col])
        else:
            series_dtype = str(df[col].dtype)
            if dtype_conversions.get(series_dtype):
                if series_dtype == "object":
                    df[col] = df[col].fillna("")
                df[col] = optimize_dtype(
                    df[col], dtype_conversions.get(series_dtype)
                )

    with Pool() as pool:
        df["Description_tr"] = pool.map(
            clean_text, df["Description"].fillna("")
        )

    df["Time to Resolve"] = (
        df["Resolved"].fillna(value=utc.localize(dt.utcnow())) - df["Created"]
    ).dt.days

    return df


def calculate_ttr(resolved: dt, created: dt):
    """ Calculates how many days spent for issue resolution.

    Parameters:
    ----------
    resolved:
        Date of issue resolution.
    created:
        Date of issue creation.

    Returns:
    ----------
        Days count spent for issue resolution.
            """
    if not resolved:
        return 0
    ttr = resolved - created
    return ttr.days
