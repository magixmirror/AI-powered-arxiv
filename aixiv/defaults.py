__all__ = [
    # constants (article)
    "CONCURRENCY",
    "TIMEOUT",
    # constants (search)
    "CATEGORIES",
    "KEYWORDS",
    "START",
    "END",
    "FORMATTING",
    "MAXIMUM",
    "ORDER",
    "SORT",
    # constants (translate)
    "LANGUAGE",
    "SUMMARIZE",
    "TRANSLATOR",
]


# standard library
from typing import Literal


# constants (article)
CONCURRENCY = 4
TIMEOUT = 10


# constants (search)
CATEGORIES = ()
KEYWORDS = ()
START = "1 day ago at midnight in UTC"
END = "0 day ago at midnight in UTC"
FORMATTING = True
MAXIMUM = 1000
ORDER: Literal["descending"] = "descending"
SORT: Literal["relevance"] = "relevance"


# constants (translate)
TRANSLATOR = "aixiv.translators.Gemini"
API_KEY = "$GEMINI_API_KEY"
LANGUAGE = "auto"
SUMMARIZE = False
