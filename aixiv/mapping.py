__all__ = ["amap"]


# standard library
from asyncio import Semaphore, gather, run
from collections.abc import Callable, Iterable
from inspect import iscoroutinefunction
from logging import getLogger
from typing import TypeVar


# dependencies
from .defaults import N_CONCURRENT


# type hints
T = TypeVar("T")


# constants
LOGGER = getLogger(__name__)


def amap(
    func: Callable[[T], T],
    objects: Iterable[T],
    /,
    *,
    n_concurrent: int = N_CONCURRENT,
) -> list[T]:
    """Map function that also supports coroutines.

    Args:
        func: Mapping function or coroutine.
        objects: Objects to be mapped.
        n_concurrent: Number of concurrent executions.
            Only used when ``func`` is a coroutine.

    Returns:
        List of mapped objects by ``func``.

    """
    if not iscoroutinefunction(func):
        return list(map(func, objects))

    sem = Semaphore(n_concurrent)

    async def wrapper(obj):
        async with sem:
            return await func(obj)

    async def main() -> list[T]:
        coros = map(wrapper, objects)
        return list(await gather(*coros))

    return run(main())
