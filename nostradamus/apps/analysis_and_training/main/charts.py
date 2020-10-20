import pandas as pd

PERIOD_MAPPING = {
    "Day": "D",
    "Week": "W-MON",
    "Month": "M",
    "3 Months": "3M",
    "6 Months": "6M",
    "Year": "Y",
}

PERIOD_FORMAT_MAPPING = {
    "Day": "%d.%m.%Y",
    "Week": "%d.%m.%Y",
    "Month": "%b %Y",
    "3 Months": "%b %Y",
    "6 Months": "%b %Y",
    "Year": "%Y",
}


def get_defect_submission(issues: pd.DataFrame, period: str) -> dict:
    """Calculates coordinates for defect submission chart.

    Parameters:
    ----------
    issues:
        Bug reports.
    period:
        Time period to be used in calculations.

    Returns:
    ----------
        Chart coordinates.
    """
    chart_period = PERIOD_MAPPING[period]
    date_format = PERIOD_FORMAT_MAPPING[period]

    issues.set_index(issues["Created"], inplace=True)
    coordinates = issues["Key"].resample(chart_period).count().cumsum()

    # Resolved line coordinates must match with Created line coordinates
    resolved_coordinates = get_resolution_coordinates(
        issues.dropna(), coordinates, date_format
    )

    coordinates.index = coordinates.index.strftime(date_format)
    created_coordinates = coordinates.to_dict()

    return {
        "created_line": created_coordinates,
        "resolved_line": resolved_coordinates,
    }


def get_resolution_coordinates(
    issues: pd.DataFrame, coordinates: pd.Series, date_format: str
) -> dict:
    """Calculates coordinates for Resolution line.

    Parameters:
    ----------
    issues:
        Bug reports.
    coordinates:
        Created coordinates.
    date_format:
        Format of date conversion.

    Returns:
    ----------
        Resolution line coordinates.
    """
    result = {}

    for date in coordinates.index:
        result[date.strftime(date_format)] = len(
            issues[
                issues["Resolved"]
                <= date.replace(hour=23, minute=59, second=59)
            ]
        )

    return result


def get_max_amount(chart_details: dict) -> dict:
    """Calculates a maximum amount of Created and Resolved issues.

    Parameters:
    ----------
    chart_details:
        Chart coordinates.

    Returns:
    ----------
        Total counts.
    """
    max_amounts = {
        "created_total_count": max(chart_details["created_line"].values()),
        "resolved_total_count": max(chart_details["resolved_line"].values()),
    }

    return max_amounts
