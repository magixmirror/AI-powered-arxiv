__all__ = ["Article", "TArticle", "amap"]


# standard library
from asyncio import Semaphore, TimeoutError, gather, run, wait_for
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass, field, replace
from logging import getLogger
from reprlib import Repr
from typing import Optional, TypeVar, Union


# dependencies
from arxiv import Result
from typing_extensions import Self
from .defaults import CONCURRENCY, TIMEOUT


# type hints
TArticle = TypeVar("TArticle", bound="Article")
Finally = Union[TArticle, Awaitable[TArticle]]


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

    def __format__(self, format_spec: str, /) -> str:
        """Support shortened representation of the article."""
        if not format_spec:
            return super().__format__(format_spec)
        else:
            return Repr(maxother=int(format_spec)).repr(self)


def amap(
    func: Callable[[TArticle], Finally[TArticle]],
    articles: Iterable[TArticle],
    /,
    *,
    concurrency: int = CONCURRENCY,
    timeout: float = TIMEOUT,
) -> list[TArticle]:
    """Article-to-article map function.

    Args:
        func: Function or coroutine function for mapping.
        articles: Articles to be mapped.
        concurrency: Number of concurrent executions.
            Only used when ``func`` is a coroutine function.
        timeout: Timeout per article in seconds.
            Only used when ``func`` is a coroutine function.

    Returns:
        List of mapped articles by ``func`` with each
        original article stored in the ``origin`` attribute.
        If timeout occurs, the original article is returned.

    """

    async def afunc(article: TArticle, /) -> TArticle:
        if isinstance(result := func(article), Awaitable):
            return replace(await result, origin=article)
        else:
            return replace(result, origin=article)

    async def main() -> list[TArticle]:
        sem = Semaphore(concurrency)

        async def runner(article: TArticle, /) -> TArticle:
            async with sem:
                try:
                    LOGGER.debug(f"Start processing {article:100}.")
                    return await wait_for(afunc(article), timeout)
                except TimeoutError:
                    LOGGER.warning(
                        f"Timeout in processing {article:100}."
                        "The original article was returned instead."
                    )
                    return article
                finally:
                    LOGGER.debug(f"Finish processing {article:100}.")

        return list(await gather(*map(runner, articles)))

    return run(main())
