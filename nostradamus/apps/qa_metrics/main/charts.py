import pandas as pd


def calculate_priority_percentage(series: pd.Series, classes: list) -> dict:
    """ Calculates percentage for values in priority predictions.

    Parameters:
    ----------
    series:
        Priority predictions.
    classes:
        Priority classes.

    Returns:
    ----------
        Percentage for priority predictions values.
    """
    percentage = calculate_percentage(series).to_dict()

    for priority in classes:
        if priority not in percentage:
            percentage[priority] = 0

    return percentage


def calculate_aot_percentage(series: pd.Series) -> dict:
    """ Calculates percentage for values in area of testing predictions.

    Parameters:
    ----------
    series:
        Area of testing predictions.

    Returns:
    ----------
        Percentage for area of testing predictions values.
    """
    percentage = calculate_percentage(series).to_dict()

    return percentage


def calculate_ttr_percentage(series: pd.Series, classes: list) -> dict:
    """ Calculates percentage for values in time to resolve predictions.

    Parameters:
    ----------
    series:
        Priority predictions.
    classes:
        Time to resolve classes

    Returns:
    ----------
        Percentage for time to resolve predictions values.
    """
    percentage = calculate_percentage(series).to_dict()

    for ttr in classes:
        if ttr not in percentage:
            percentage[ttr] = 0

    return percentage


def calculate_resolution_percentage(df: pd.DataFrame, classes: dict) -> dict:
    """ Calculates percentage by values for resolution predictions.

    Parameters:
    ----------
    df:
        Bugs.
    classes:
        Resolution classes.

    Returns:
    ----------
        Percentage for resolutions predictions values.
    """
    percentage = dict()
    for resolution in classes:
        percentage[resolution] = calculate_percentage(
            df["Resolution: " + resolution]
        ).to_dict()
        for class_ in classes[resolution]:
            if class_ not in percentage[resolution]:
                percentage[resolution][class_] = 0

    return percentage


def calculate_percentage(bug_attributes: pd.Series) -> pd.Series:
    """ Calculates percentage for series values.

    Parameters:
    ----------
    bug_attributes:
        Pandas series.

    Returns:
    ----------
        Rounded values percentage.
    """
    return (
        (bug_attributes.value_counts(normalize=True) * 100).round().astype(int)
    )
