from typing import List

from pandas import qcut, get_dummies, Categorical, DataFrame
from training.common import check_required_percentage
from database.users.settings import ModelClasses


def filter_classes(
    issues: DataFrame, areas_of_testing: List[str], resolution: List[str]
) -> ModelClasses:
    """Filters out classes with inadequate percentage of representatives.

    :param issues: Bug reports.
    :param areas_of_testing: Areas of testing classes;
    :param resolution: Resolution classes.
    :return: Classes of models.
    """
    classes = {
        "areas_of_testing": areas_of_testing,
        "Resolution": resolution,
        "Priority": issues["Priority"].unique().tolist(),
        "Time to Resolve": issues["Time to Resolve"].unique().tolist(),
    }

    filtered_classes = {}
    for metric in classes.keys():
        if metric == "areas_of_testing":
            filtered_classes[metric] = [
                el
                for el in classes[metric]
                if check_required_percentage(issues[el], 1)
                and len(set(issues[el])) != 1
            ]
        else:
            filtered_classes[metric] = sorted(
                [
                    el
                    for el in classes[metric]
                    if check_required_percentage(issues[metric], el)
                    and len(set(issues[metric])) != 1
                ]
            )

    return filtered_classes


def encode_series(issues: DataFrame) -> DataFrame:
    """Encodes series classes.

    :param issues: Bug reports.
    :return: Dataframe containing encoded series.
    """

    # TODO Investigation is required for imbalanced data
    issues["Time to Resolve"] = qcut(
        issues["Time to Resolve"].astype(int), q=4, duplicates="drop"
    )
    issues["time to resolve_codes"] = issues["Time to Resolve"].cat.rename_categories(
        range(len(issues["Time to Resolve"].unique()))
    )

    issues["priority_codes"] = Categorical(issues["Priority"], ordered=True).codes

    issues = issues.reset_index(drop=True)
    series_resolution = issues["Resolution"]
    issues = get_dummies(issues, columns=["Resolution"])
    issues["Resolution"] = series_resolution

    return issues
