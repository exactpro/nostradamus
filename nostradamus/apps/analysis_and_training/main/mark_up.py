import pandas as pd
from multiprocessing.dummy import Pool


def mark_up_series(
    issues: pd.DataFrame, series: str, area_of_testing: str, patterns: str
) -> pd.DataFrame:
    """ Appends binarized series to df.

    Parameters:
    ----------
    issues:
        Bug reports.
    series:
        df series name.
    area_of_testing:
        area of testing.
    patterns:
        searching elements.

    Returns:
    --------
        The whole df with binarized series.

    """
    with Pool() as pool:
        issues[area_of_testing] = [
            pool.apply_async(binarize_value, (el, patterns,)).get()
            for el in issues[series]
        ]
    return issues


def binarize_value(df_element: str, patterns: str) -> int:
    """ Binarizes searching value.

    Parameters:
    ----------
    df_element:
        searching source.
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
    issues: pd.DataFrame, marked_up_series: str
) -> pd.DataFrame:
    """ Marks up series which represents data that isn't related to marked up fields.

    Parameters:
    ----------
    issues:
        Bug reports.
    marked_up_series:
        Names of marked up series.

    Returns:
        The whole dataframe with new series appended.
    """
    issues["Other"] = "0"
    issues["Other"] = (
        issues["Other"]
        .replace(["0"], "1")
        .where(issues[marked_up_series].sum(axis=1) == 0, 0)
        .apply(int)
    )
    return issues
