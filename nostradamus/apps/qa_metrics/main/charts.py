from typing import List, Dict

import pandas as pd


def calculate_priority_percentage(
    priority_predictions: pd.Series, classes: List[str]
) -> Dict[str, int]:
    """Calculates percentage for values in priority predictions.

    Parameters:
    ----------
    priority_predictions:
        Priority predictions.
    classes:
        Priority classes.

    Returns:
    ----------
        Percentage for priority predictions values.
    """
    percentage = calculate_percentage(priority_predictions).to_dict()

    for priority in classes:
        if priority not in percentage:
            percentage[priority] = 0

    return percentage


def calculate_aot_percentage(
    aot_predictions: pd.Series, areas_of_testing: List[str]
) -> Dict[str, int]:
    """Calculates percentage for values in area of testing predictions.

    Parameters:
    ----------
    aot_predictions:
        Area of testing predictions.
    areas_of_testing:
        Areas of testing.

    Returns:
    ----------
        Percentage for area of testing predictions values.
    """
    percentage = calculate_percentage(aot_predictions).to_dict()

    for area_of_testing in areas_of_testing:
        if area_of_testing not in percentage:
            percentage[area_of_testing] = 0

    return percentage


def calculate_ttr_percentage(
    ttr_predictions: pd.Series, classes: List[str]
) -> Dict[str, int]:
    """Calculates percentage for values in time to resolve predictions.

    Parameters:
    ----------
    ttr_predictions:
        Time to resolve predictions.
    classes:
        Time to resolve classes

    Returns:
    ----------
        Percentage for time to resolve predictions values.
    """
    percentage = calculate_percentage(ttr_predictions).to_dict()

    for ttr in classes:
        if ttr not in percentage:
            percentage[ttr] = 0

    return percentage


def calculate_resolution_percentage(
    issues: pd.DataFrame,
    classes: Dict[str, List[str]],
) -> Dict[str, Dict[str, int]]:
    """Calculates percentage by values for resolution predictions.

    Parameters:
    ----------
    issues:
        Issues' attributes.
    classes:
        Resolution classes.

    Returns:
    ----------
        Percentage for resolutions predictions.
    """
    percentage = dict()
    for resolution in classes:
        percentage[resolution] = calculate_percentage(
            issues["Resolution: " + resolution]
        ).to_dict()
        for class_ in classes[resolution]:
            if class_ not in percentage[resolution]:
                percentage[resolution][class_] = 0

    return percentage


def calculate_percentage(issue_attributes: pd.Series) -> pd.Series:
    """Calculates percentage for series values.

    Parameters:
    ----------
    issue_attributes:
        Pandas series.

    Returns:
    ----------
        Rounded values percentage.
    """
    return (
        (issue_attributes.value_counts(normalize=True) * 100)
        .round()
        .astype(int)
    )
