import pandas as pd
from multiprocessing import Pool


def mark_up_series(
    df: pd.DataFrame, series: str, area_of_testing: str, patterns: str
) -> pd.DataFrame:
    """ Appends binarized series to df.

    Parameters:
    ----------
        df: 
            Bug reports;
        series: 
            df series name;
        area_of_testing: 
            area of testing;
        patterns: 
            searching elements.

    Returns:
    --------
        The whole df with binarized series.

    """
    with Pool() as pool:
        df[area_of_testing] = [
            pool.apply_async(binarize_value, (el, patterns,)).get()
            for el in df[series]
        ]
    return df


def binarize_value(df_element: str, patterns: str) -> int:
    """ Binarizes searching value.

    Parameters:
    ----------
        df_element: 
            searching source;
        patterns: 
            searching elements.

    Returns:
    ----------
        Binarized value.

    """
    for pattern in patterns:
        if pattern.strip() in str(df_element).split(","):
            return 1
    return 0


def mark_up_other_data(
    df: pd.DataFrame, marked_up_series: str
) -> pd.DataFrame:
    """ Marks up series which represents data that isn't related to marked up fields.

    Parameters:
    ----------
        df: 
            Bug reports;
        marked_up_series: 
            names of marked up series.

    Returns:
        The whole dataframe with new series appended.

    """
    df["Other"] = "0"
    df["Other"] = (
        df["Other"]
        .replace(["0"], "1")
        .where(df[marked_up_series].sum(axis=1) == 0, 0)
        .apply(int)
    )
    return df
