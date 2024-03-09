__all__ = ["Article", "TArticle"]


# standard library
from dataclasses import dataclass, field
from logging import getLogger
from typing import Optional, TypeVar


# dependencies
from arxiv import Result
from typing_extensions import Self


# type hints
T = TypeVar("T")
TArticle = TypeVar("TArticle", bound="Article")


# constants
LOGGER = getLogger(__name__)


@dataclass(frozen=True)
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
        LOGGER.debug(f"Article created from: {result!r}")

        return cls(
            title=result.title,
            authors=[author.name for author in result.authors],
            summary=result.summary,
            url=result.entry_id,
        )
