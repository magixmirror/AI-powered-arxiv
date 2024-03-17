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
    "API_KEY",
    "SUMMARIZE",
    "TRANSLATOR",
]


# standard library
from typing import Literal


# constants (article)
CONCURRENCY = 4
"""Number of concurrent executions."""

TIMEOUT = 10
"""Timeout per article in seconds."""


# constants (search)
CATEGORIES = ()
"""arXiv categories."""

KEYWORDS = ()
"""Keywords of the search."""

START = "1 day ago at midnight in UTC"
"""Start date (and time) of the search."""

END = "0 day ago at midnight in UTC"
"""End date (and time) of the search."""

FORMATTING = True
"""Whether to format articles."""

MAXIMUM = 1000
"""Maximum number of articles to return."""

ORDER: Literal["descending"] = "descending"
"""Sort order of the search results."""

SORT: Literal["relevance"] = "relevance"
"""Sort criterion of the search results."""

# constants (translate)
TRANSLATOR = "aixiv.translators.Gemini"
"""Translator class or the path for it."""

API_KEY = "$GOOGLE_API_KEY"
"""API key or the environment variable for it."""

LANGUAGE = "auto"
"""Language code of the translated articles."""

SUMMARIZE = False
"""Whether to summarize the articles."""
