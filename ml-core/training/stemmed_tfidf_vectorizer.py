from dataclasses import dataclass
from typing import FrozenSet

from sklearn.feature_extraction.text import TfidfVectorizer
from Stemmer import Stemmer

from sklearn.feature_extraction import text

WEEKDAYS_SW = [
    "monday",
    "mon",
    "tuesday",
    "tue",
    "wednesday",
    "wed",
    "thursday",
    "thu",
    "friday",
    "fri",
    "saturday",
    "sat",
    "sunday",
    "sun",
]

MONTHS_SW = [
    "january",
    "jan",
    "february",
    "feb",
    "march",
    "mar",
    "april",
    "apr",
    "may",
    "june",
    "jun",
    "july",
    "jul",
    "august",
    "aug",
    "september",
    "sep",
    "october",
    "oct",
    "november",
    "nov",
    "december",
    "dec",
]

STOP_WORDS = text.ENGLISH_STOP_WORDS.difference(("see", "system", "call")).union(
    WEEKDAYS_SW, MONTHS_SW, ["having", "couldn"]
)


ENG_STEMMER = Stemmer("eng")


@dataclass(init=False)
class StemmedTfidfVectorizer(TfidfVectorizer):
    norm: str = "l2"
    sublinear_tf: bool = True
    min_df: int = 1
    stop_words: FrozenSet[str] = STOP_WORDS
    analyzer = "word"

    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: ENG_STEMMER.stemWords(analyzer(doc))
