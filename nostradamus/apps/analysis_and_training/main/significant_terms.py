import pandas as pd
import numpy as np
from typing import Dict, List, Union
from pandas import DataFrame
from sklearn import feature_selection
from sklearn.feature_selection import SelectKBest

from apps.analysis_and_training.main.common import get_stop_words

from utils.stemmed_tfidf_vectorizer import StemmedTfidfVectorizer

from collections import OrderedDict

from apps.analysis_and_training.main.common import check_required_percentage
from apps.analysis_and_training.main.mark_up import mark_up_series
from utils.warnings import (
    SignificantTermsCantCalculateWarning,
    SignificantTermsLessOnePercentWarning,
    SignificantTermsMetricDoesntExist,
)

SIGNIFICANT_TERMS_METRICS = ["Resolution", "Priority"]

MarkUpEntities = List[Dict[str, Union[List[str], str]]]
BugResolutions = List[Dict[str, str]]
AreaOfTesting = Dict[str, Union[str, MarkUpEntities, BugResolutions]]
SignificantTerms = Dict[str, Union[List[str], str, Dict[str, int]]]


def calculate_significance_weights(
    issues: pd.DataFrame, metric: str
) -> Dict[str, float]:
    """Calculates top terms based on significance weights.

    :param issues: Bug reports.
    :param metric: Value which is used for calculations.
    :return: First 20 calculated terms with their weights.
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


def get_term_metrics(issues: pd.DataFrame, aot: AreaOfTesting) -> List[str]:
    """Generates metrics for significant terms calculation.

    :param issues: Bug reports.
    :param aot: Areas of testing.
    :return: Metrics represented as Metric Value pairs.
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


def get_significant_terms(
    issues: pd.DataFrame, aot: AreaOfTesting = None
) -> SignificantTerms:
    """Generates content for significant terms card.

    :param issues: Bug reports.
    :param aot: Areas of testing.
    :return:Object with calculated terms, all available metrics
            and one metric separately based on which terms have been calculated.
            By default calculations are performed for the first populated metric.
    """

    # Can't be calculated on dataset containing less than 100 bugs
    if len(issues) < 100:
        raise SignificantTermsCantCalculateWarning

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


def get_top_terms(issues: DataFrame, metric: str) -> Dict[str, float]:
    """Calculates top terms.

    :param issues: Bug reports.
    :param metric: Value which is used for calculations.
    :return: Object with calculated terms.
    """
    chi2 = feature_selection.chi2

    sw = get_stop_words(issues)
    tfidf = StemmedTfidfVectorizer(stop_words=sw)
    tfs = tfidf.fit_transform(issues["Description_tr"])

    y = issues[metric]
    selector = SelectKBest(score_func=chi2, k="all")
    selector.fit_transform(tfs, y)

    return dict(zip(tfidf.get_feature_names(), selector.scores_))


def calculate_top_terms(issues: DataFrame, metric: str) -> List[str]:
    """Calculates top terms which are based on significance weights.

    :param issues: Bug reports.
    :param metric: Field which is used for calculation.
    :return: List of the calculated terms.
    """
    terms = get_top_terms(issues, metric)

    terms = {k: v for (k, v) in terms.items() if v > 1}
    return [k for (k, v) in terms.items() if v > np.mean(list(terms.values()))]


def check_standard_metric(issues: DataFrame, metric: str) -> None:
    """Checks whether exist the standard metric.

    :param issues: Bug reports.
    :param metric: Field which is used for calculation.
    """
    split_metric = metric.split()
    series = issues[split_metric[0]]
    category = " ".join(split_metric[1:])
    if category in series.dropna().unique().tolist():
        if not check_required_percentage(series, category):
            raise SignificantTermsLessOnePercentWarning
    else:
        raise SignificantTermsMetricDoesntExist


def check_aot_metric(
    issues: DataFrame,
    metric: str,
    source_field: str,
    mark_up_entities: MarkUpEntities,
) -> None:
    """Checks whether exist the area of testing metric.

    :param issues: Bug reports.
    :param metric: Field which is used for calculation.
    :param source_field: Source Field.
    :param mark_up_entities: Area of Testing.
    """
    if source_field and mark_up_entities:
        for area in mark_up_entities:
            if area["area_of_testing"] in [metric, metric.split()[0]]:
                issues = mark_up_series(
                    issues,
                    source_field,
                    area["area_of_testing"],
                    area["entities"],
                )
                if not check_required_percentage(
                    issues[area["area_of_testing"]], 1
                ):
                    raise SignificantTermsLessOnePercentWarning
                break
        else:
            raise SignificantTermsMetricDoesntExist
    else:
        raise SignificantTermsMetricDoesntExist
