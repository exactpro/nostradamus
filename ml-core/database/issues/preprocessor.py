import pandas as pd


def optimize_dtype(
    series: pd.Series,
    dtype: str,
) -> pd.Series:
    """Automatically converts series to handled data type.

    :param series: Series to be converted.
    :param dtype: Data type is used for conversion.
    :return: Optimized pandas series.
    """
    return series.astype(dtype)


def convert_date(raw_dates: pd.Series) -> pd.Series:
    """Automatically converts series containing raw dates
    to specific format.

    :param raw_dates: Series to be converted.
    :return: Optimized pandas series.
    """
    raw_dates = pd.to_datetime(raw_dates, utc=True)
    return raw_dates


DTYPE_CONVERSIONS = {
    "date": convert_date,
    "int": "int32",
    "float": "float32",
    "unique": "category",
    "string": str,
    "object": str,
    "float64": "float32",
    "int64": "int32",
}

BUG_ATTRIBUTES = {
    "built-in": {
        "Labels": "string",
        "Summary": "string",
        "Description": "string",
        "Components": "string",
        "Attachments": "int",
        "Comments": "int",
        "Project": "unique",
        "Priority": "unique",
        "Status": "unique",
        "Key": "unique",
        "Resolution": "unique",
    },
    "raw": {"Resolved": "date", "Created": "date", "Updated": "date"},
}


def preprocess_df(issues: pd.DataFrame) -> pd.DataFrame:
    """Basic DataFrame preprocessing:
        - datatypes optimization;
        - text cleaning.

    :param issues: Bug reports.
    :return: Preprocessed issues.
    """
    built_in_dtypes = BUG_ATTRIBUTES.get("built-in")
    raw_dtypes = BUG_ATTRIBUTES.get("raw")

    for col in issues.columns:
        if built_in_dtypes.get(col):
            issues[col] = optimize_dtype(
                issues[col], DTYPE_CONVERSIONS.get(built_in_dtypes.get(col))
            )
        elif raw_dtypes.get(col):
            issues[col] = DTYPE_CONVERSIONS.get(raw_dtypes.get(col))(issues[col])
        else:
            series_dtype = str(issues[col].dtype)
            if DTYPE_CONVERSIONS.get(series_dtype):
                if series_dtype == "object":
                    issues[col] = issues[col].fillna("")
                issues[col] = optimize_dtype(
                    issues[col], DTYPE_CONVERSIONS.get(series_dtype)
                )

    return issues
