__all__ = ["Article", "search"]


# standard library
from collections.abc import Sequence
from dataclasses import dataclass, field
from logging import getLogger
from typing import Optional


# dependencies
from arxiv import Client, Result, Search
from dateparser import parse
from typing_extensions import Self


# constants
ARXIV_DATE_FORMAT = "%Y%m%d%H%M%S"
LOGGER = getLogger(__name__)


@dataclass
class Article:
    """Article information."""

    title: str
    """Title of the article."""

    authors: list[str]
    """Authors of the article."""

    summary: str
    """Summary of the article."""

    url: str
    """URL of the article."""

    origin: Optional[Self] = field(default=None, repr=False)
    """Original article (if it exists)."""

    @classmethod
    def from_arxiv(cls, result: Result, /) -> Self:
        """Create an article from an arXiv query result."""
        return cls(
            title=result.title,
            authors=[author.name for author in result.authors],
            summary=result.summary,
            url=str(result),
        )


def search(
    categories: Sequence[str],
    keywords: Sequence[str] = (),
    start_date: str = "3 days ago at midnight in UTC",
    end_date: str = "2 days ago at midnight in UTC",
) -> list[Article]:
    """Search for articles in arXiv.

    Args:
        categories: arXiv categories.
        keywords: Keywords of the search.
        start_date: Start date of the search.
        end_date: End date of the search.

    Returns:
        Articles found with given conditions.

    """
    start_date = format_date(start_date)
    end_date = format_date(end_date)

    query = f"submittedDate:[{start_date} TO {end_date}]"

    if categories:
        sub = " OR ".join(f"cat:{cat}" for cat in categories)
        query += f" AND ({sub})"

    if keywords:
        sub = " OR ".join(f'abs:"{kwd}"' for kwd in keywords)
        query += f" AND ({sub})"

    client = Client()
    search = Search(query)
    results = list(client.results(search))
    LOGGER.debug(f"Query for search: {query!r}")
    LOGGER.debug(f"Number of articles found: {len(results)}")

    return list(map(Article.from_arxiv, results))


def format_date(date_like: str, /) -> str:
    """Parse and format a date-like string."""
    if (dt := parse(date_like)) is not None:
        return dt.strftime(ARXIV_DATE_FORMAT)

    raise ValueError(f"Could not parse {date_like!r}.")
