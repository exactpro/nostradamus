import pandas as pd
import numpy as np

from collections import OrderedDict

from apps.analysis_and_training.main.common import check_required_percentage
from apps.analysis_and_training.main.training import get_top_terms
from utils.const import SIGNIFICANT_TERMS_METRICS


def calculate_significance_weights(df: pd.DataFrame, metric: str) -> dict:
    """ Calculates top terms based on significance weights.

    Parameters:
    ----------
    df:
        Bug reports.
    metric:
        Value which is used for calculations.

    Returns:
    ----------
        First 20 calculated terms with their weights.
    """

    if metric.split()[0] in ("Resolution", "Priority"):
        df = pd.get_dummies(
            df, prefix=[metric.split()[0]], columns=[metric.split()[0]]
        )
        metric = metric.split()[0] + "_" + " ".join(metric.split()[1:])

    calculated_terms = get_top_terms(df, metric)

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


def get_term_metrics(df: pd.DataFrame, aot: dict):
    """ Generates metrics for significant terms calculation.

    Parameters:
    ----------
    df:
        Bug reports.
    aot:
        Areas of testing.
    Returns:
    ----------
        Metrics represented as Metric Value pairs.
    """

    metrics = []

    for metric in SIGNIFICANT_TERMS_METRICS:
        el_series = df[metric]
        for category in el_series.dropna().unique().tolist():
            if category and check_required_percentage(el_series, category):
                metrics.append(" ".join([metric, category]))

    if aot:
        aot_metrics = [
            area["area_of_testing"] for area in aot["mark_up_entities"]
        ]
        metrics.extend(aot_metrics)

    return metrics


def get_significant_terms(df: pd.DataFrame, aot: dict = None) -> dict:
    """ Generates all required data for significant terms view.

    Parameters:
    ----------
    df:
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
    if len(df) < 100:

        # TODO need decide how to return exceptions separately
        # TODO raise exception if dataframe length is less than 100
        return {"referring_to": [], "chosen_metric": "", "terms": {}}

    metrics = get_term_metrics(df, aot)

    if metrics:
        chosen_metric = metrics[0]
        terms = calculate_significance_weights(df, chosen_metric)
    else:
        chosen_metric = ""
        terms = {}

    significant_terms = {
        "metrics": metrics,
        "chosen_metric": chosen_metric,
        "terms": terms,
    }

    return significant_terms
