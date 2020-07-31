import pandas as pd

from datetime import datetime as dt

from apps.extractor.main.connector import get_issues
from utils.const import bug_attributes, dtype_conversions
from utils.data_converter import optimize_dtype


def preprocess_df(issues: pd.DataFrame) -> pd.DataFrame:
    """Basic DataFrame preprocessing:
        - datatypes optimization;
        - text cleaning.

    Parameters
    ----------
    issues:
        Bug reports.

    Returns
    -------
        Preprocessed issues.
    """
    built_in_dtypes = bug_attributes.get("built-in")
    raw_dtypes = bug_attributes.get("raw")

    for col in issues.columns:
        if built_in_dtypes.get(col):
            issues[col] = optimize_dtype(
                issues[col], dtype_conversions.get(built_in_dtypes.get(col))
            )
        elif raw_dtypes.get(col):
            issues[col] = dtype_conversions.get(raw_dtypes.get(col))(
                issues[col]
            )
        else:
            series_dtype = str(issues[col].dtype)
            if dtype_conversions.get(series_dtype):
                if series_dtype == "object":
                    issues[col] = issues[col].fillna("")
                issues[col] = optimize_dtype(
                    issues[col], dtype_conversions.get(series_dtype)
                )

    return issues


def calculate_ttr(resolved: dt, created: dt) -> int:
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

    if resolved > created:
        return (resolved - created).days

    return 0


def get_issues_dataframe(
    fields: list = None, filters: list = None
) -> pd.DataFrame:
    """ Converts issues to optimized pandas dataframe.

    Parameters:
    ----------
    fields:
        Issue fields.
    filters:
        Filters to be applied.

    Returns:
    ----------
        Optimized issues.
    """
    issues = pd.DataFrame(get_issues(fields=fields, filters=filters))

    return preprocess_df(issues)
