import numpy
from typing import List, Dict

from pandas import DataFrame
from sklearn import feature_selection
from sklearn.feature_selection import SelectKBest
from training.stop_words import get_stop_words
from training.stemmed_tfidf_vectorizer import StemmedTfidfVectorizer


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

    return [k for (k, v) in terms.items() if v > numpy.mean(list(terms.values()))]
