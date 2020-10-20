import pandas as pd
import numpy as np

from collections import OrderedDict

from apps.analysis_and_training.main.common import check_required_percentage
from apps.analysis_and_training.main.mark_up import mark_up_series
from apps.analysis_and_training.main.training import get_top_terms

SIGNIFICANT_TERMS_METRICS = ["Resolution", "Priority"]


def calculate_significance_weights(issues: pd.DataFrame, metric: str) -> dict:
    """Calculates top terms based on significance weights.

    Parameters:
    ----------
    issues:
        Bug reports.
    metric:
        Value which is used for calculations.

    Returns:
    ----------
        First 20 calculated terms with their weights.
    """

    if metric.split()[0] in ("Resolution", "Priority"):
        issues = pd.get_dummies(
            issues, prefix=[metric.split()[0]], columns=[metric.split()[0]]
        )
        metric = metric.split()[0] + "_" + " ".join(metric.split()[1:])

    calculated_terms = get_top_terms(issues, metric)

    for term in calculated_terms:
        if np.isnan(calculated_terms[term]):
            calculated_terms[term] = np.nan_to_num(
                calculated_terms[term], nan=1.0
            )

    calculated_terms = OrderedDict(
        (k, v)
        for k, v in sorted(
            set(calculated_terms.items()), key=lambda x: x[1], reverse=True
        )
    )
    return dict(list(calculated_terms.items())[:20])


def get_term_metrics(issues: pd.DataFrame, aot: dict) -> list:
    """Generates metrics for significant terms calculation.

    Parameters:
    ----------
    issues:
        Bug reports.
    aot:
        Areas of testing.

    Returns:
    ----------
        Metrics represented as Metric Value pairs.
    """

    metrics = []

    for metric in SIGNIFICANT_TERMS_METRICS:
        series = issues[metric]
        for category in series.dropna().unique().tolist():
            if category and check_required_percentage(series, category):
                metrics.append(" ".join([metric, category]))

    if aot:
        aot_metrics = []
        for area in aot["mark_up_entities"]:
            series = mark_up_series(
                issues, aot["source_field"], "aot", area["entities"]
            ).aot
            if check_required_percentage(series, 1):
                aot_metrics.append(area["area_of_testing"])

        metrics.extend(aot_metrics)

    return metrics


def get_significant_terms(issues: pd.DataFrame, aot: dict = None) -> dict:
    """Generates content for significant terms card.

    Parameters:
    ----------
    issues:
        Bug reports.
    aot:
        Areas of testing.

    Returns:
    ----------
        Object with calculated terms, all available metrics
        and one metric separately based on which terms have been calculated.
        By default calculations are performed for the first populated metric
    """

    # Can't be calculated on dataset containing less than 100 bugs
    if len(issues) < 100:

        # TODO raise exception if dataframe length is less than 100
        return {"metrics": [], "chosen_metric": "", "terms": {}}

    metrics = get_term_metrics(issues, aot)

    if metrics:
        chosen_metric = metrics[0]
        terms = calculate_significance_weights(issues, chosen_metric)
    else:
        chosen_metric = ""
        terms = {}

    significant_terms = {
        "metrics": metrics,
        "chosen_metric": chosen_metric,
        "terms": terms,
    }

    return significant_terms
