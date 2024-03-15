__all__ = ["Article", "TArticle", "amap"]


# standard library
from asyncio import (
    Semaphore,
    TimeoutError,
    gather,
    iscoroutinefunction,
    run,
    wait_for,
)
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass, field, replace
from logging import getLogger
from textwrap import shorten
from typing import Optional, TypeVar, Union


# dependencies
from arxiv import Result
from typing_extensions import Self
from .defaults import CONCURRENCY, TIMEOUT


# type hints
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


def amap(
    func: Union[
        Callable[[TArticle], TArticle],
        Callable[[TArticle], Awaitable[TArticle]],
    ],
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
    sem = Semaphore(concurrency)

    async def afunc(article: TArticle) -> TArticle:
        if iscoroutinefunction(func):
            new = await func(article)
        else:
            new = func(article)

        return replace(new, origin=article)  # type: ignore

    async def runner(article: TArticle) -> TArticle:
        func_name = func.__qualname__
        func_args = shorten(str(article), 50)

        async with sem:
            try:
                LOGGER.debug(f"{func_name}({func_args}) started.")
                return await wait_for(afunc(article), timeout)
            except TimeoutError:
                LOGGER.warning(
                    f"{func_name}({func_args}) has timed out. "
                    "The original article was returned instead."
                )
                return article
            finally:
                LOGGER.debug(f"{func_name}({func_args}) finished.")

    async def main() -> list[TArticle]:
        return list(await gather(*map(runner, articles)))

    return run(main())
