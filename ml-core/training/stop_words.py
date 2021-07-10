from typing import List, FrozenSet, Set, Any

from pandas import DataFrame

from training.stemmed_tfidf_vectorizer import STOP_WORDS
from itertools import chain


def unpack_lists(lists: List[List]) -> List[Any]:
    """Unpacks two-dimensional lists to one-dimensional.

    :param lists: two-dimensional list.
    :return: Unpacked one-dimensional list.
    """
    return list(chain(*lists))


def get_assignee_reporter(issues: DataFrame) -> Set[str]:
    """Parsing full names from Assignee and Reported series.

    :param issues: Bug reports.
    :return: Unique names and last names.
    """
    full_names = [
        full_name.lower().split()
        for full_name in issues["Assignee"].tolist() + issues["Reporter"].tolist()
    ]

    assignee_reporter = set(unpack_lists(full_names))

    return assignee_reporter


def get_stop_words(issues: DataFrame) -> FrozenSet[str]:
    """Generates stop words for TfidfVectorizer constructor.

    :param issues: Bug reports.
    :return: Unique words which will be ignored.
    """
    assignee_reporter = get_assignee_reporter(issues)

    return STOP_WORDS.union(assignee_reporter)
