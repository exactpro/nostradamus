import pandas as pd
from collections import OrderedDict

from apps.analysis_and_training.main.common import get_stop_words
from utils.stemmed_tfidf_vectorizer import StemmedTfidfVectorizer


def calculate_frequently_terms(df: pd.DataFrame) -> list:
    """Calculates most frequently used term.

    Parameters
    ----------
    df:
        Bug reports.

    Returns
    -------
        List of the first 100 of the most frequently used terms.
    """
    descriptions = df["Description_tr"]

    sw = get_stop_words(df)
    tfidf = StemmedTfidfVectorizer(stop_words=sw)

    try:
        tfidf.fit_transform(descriptions)
    except ValueError:
        return "Oops! Too little data to calculate."

    idf = tfidf.idf_
    freq_terms = dict(zip(tfidf.get_feature_names(), idf))
    freq_terms = OrderedDict(
        (k, v)
        for k, v in sorted(
            set(freq_terms.items()), key=lambda x: x[1], reverse=True
        )
    )
    return list(freq_terms.keys())[:100]
