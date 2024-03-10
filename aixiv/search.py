__all__ = ["Article", "format", "search"]


# standard library
from collections.abc import Iterable, Sequence
from dataclasses import replace
from logging import getLogger
from re import compile
from textwrap import shorten
from typing import Literal


# dependencies
from arxiv import Client, Search, SortCriterion, SortOrder
from dateparser import parse
from pylatexenc.latex2text import LatexNodes2Text
from .article import Article, TArticle
from .defaults import (
    KEYWORDS,
    CATEGORIES,
    START,
    END,
    FORMATTING,
    MAXIMUM,
    ORDER,
    SORT,
)
from .mapping import amap


# constants
ARXIV_DATE_FORMAT = "%Y%m%d%H%M%S"
ARXIV_LATEX_CONVERTER = LatexNodes2Text()
ARXIV_SEP_PATTERN = compile(r"\n+\s*|\n*\s+")
ARXIV_SEP_REPL = " "
LOGGER = getLogger(__name__)


def format(articles: Iterable[TArticle], /) -> list[TArticle]:
    """Format the title and summary of each article.

    Args:
        articles: Articles to be formatted.

    Returns:
        Articles with each title and summary formatted.

    """

    def inner(article: TArticle) -> TArticle:
        title = convert_latex(format_sep(article.title))
        summary = convert_latex(format_sep(article.summary))
        return replace(article, title=title, summary=summary)

    return list(amap(inner, articles))


def search(
    categories: Sequence[str] = CATEGORIES,
    keywords: Sequence[str] = KEYWORDS,
    start: str = START,
    end: str = END,
    *,
    formatting: bool = FORMATTING,
    maximum: int = MAXIMUM,
    order: Literal["ascending", "descending"] = ORDER,
    sort: Literal["lastUpdatedDate", "relevance", "submittedDate"] = SORT,
) -> list[Article]:
    """Search for articles in arXiv.

    Args:
        categories: arXiv categories.
        keywords: Keywords of the search.
        start: Start date (and time) of the search.
        end: End date (and time) of the search.
        formatting: Whether to format articles.
        maximum: Maximum number of articles to return.
        order: Sort order of the search results.
        sort: Sort criterion of the search results.

    Returns:
        Articles found with given conditions.

    """
    query = f"submittedDate:[{format_date(start)} TO {format_date(end)}]"

    if categories:
        sub = " OR ".join(f"cat:{cat}" for cat in categories)
        query += f" AND ({sub})"

    if keywords:
        sub = " OR ".join(f'abs:"{kwd}"' for kwd in keywords)
        query += f" AND ({sub})"

    client = Client()
    search = Search(
        query,
        sort_by=SortCriterion(sort),
        sort_order=SortOrder(order),
        max_results=maximum,
    )
    results = client.results(search)
    articles = list(map(Article.from_arxiv, results))
    LOGGER.debug(f"Query for search: {query!r}")
    LOGGER.debug(f"Number of articles found: {len(articles)}")

    return format(articles) if formatting else articles


def convert_latex(string: str, /) -> str:
    """Convert all LaTeX commands in a string to Unicode."""
    try:
        return ARXIV_LATEX_CONVERTER.latex_to_text(string)
    except Exception:
        LOGGER.warning(
            f"Failed to format {shorten(string, 50)!r}. "
            "The original string was returned instead."
        )
        return string


def format_date(string: str, /) -> str:
    """Format a data-like string for arXiv."""
    if (dt := parse(string)) is not None:
        return dt.strftime(ARXIV_DATE_FORMAT)

    raise ValueError(f"Failed to parse {string!r}.")


def format_sep(string: str, /) -> str:
    """Format all separators in a string."""
    return ARXIV_SEP_PATTERN.sub(ARXIV_SEP_REPL, string)
