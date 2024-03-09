__all__ = [
    # constants (article)
    "N_CONCURRENT",
    # constants (search)
    "CATEGORIES",
    "KEYWORDS",
    "START",
    "END",
    "MAXIMUM",
    "ORDER",
    "SORT",
]


# standard library
from typing import Literal


# constants (article)
N_CONCURRENT = 4


# constants (search)
CATEGORIES = ()
KEYWORDS = ()
START = "1 day ago at midnight in UTC"
END = "0 day ago at midnight in UTC"
MAXIMUM = 1000
ORDER: Literal["descending"] = "descending"
SORT: Literal["relevance"] = "relevance"
