__all__ = ["Article", "search"]


# standard library
from collections.abc import Sequence
from logging import getLogger
from typing import Literal


# dependencies
from arxiv import Client, Search, SortCriterion, SortOrder
from dateparser import parse
from .article import Article
from .defaults import KEYWORDS, CATEGORIES, START, END, MAXIMUM, ORDER, SORT


# constants
ARXIV_DATE_FORMAT = "%Y%m%d%H%M%S"
LOGGER = getLogger(__name__)


def search(
    categories: Sequence[str] = CATEGORIES,
    keywords: Sequence[str] = KEYWORDS,
    start: str = START,
    end: str = END,
    *,
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
        maximum: Maximum number of articles to return.
        order: Sort order of the search results.
        sort: Sort criterion of the search results.

    Returns:
        Articles found with given conditions.

    """
    query = f"submittedDate:[{parse_date(start)} TO {parse_date(end)}]"

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
    results = list(client.results(search))

    LOGGER.debug(f"Query for search: {query!r}")
    LOGGER.debug(f"Number of articles found: {len(results)}")
    return list(map(Article.from_arxiv, results))


def parse_date(date_like: str, /) -> str:
    """Parse a date-like string and format it for arXiv."""
    if (dt := parse(date_like)) is not None:
        return dt.strftime(ARXIV_DATE_FORMAT)

    raise ValueError(f"Failed to parse {date_like!r}.")
