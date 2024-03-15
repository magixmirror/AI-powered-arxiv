__all__ = ["Translator", "translate"]


# standard library
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from importlib import import_module
from logging import getLogger
from typing import Any, Union


# dependencies
from babel import Locale
from .article import TArticle, amap
from .defaults import CONCURRENCY, LANGUAGE, SUMMARIZE, TIMEOUT, TRANSLATOR


# constants
LANG_AUTO = "auto"
LANG_EN = "en"
LOGGER = getLogger(__name__)
PATH_SEP = "."
PATH_SPLIT = 1


def translate(
    articles: Iterable[TArticle],
    /,
    *,
    language: str = LANGUAGE,
    summarize: bool = SUMMARIZE,
    translator: Union[type["Translator"], str] = TRANSLATOR,
    concurrency: int = CONCURRENCY,
    timeout: float = TIMEOUT,
    **options: Any,
) -> list[TArticle]:
    """Translate (and summarize) articles.

    Args:
        language: Language of the translated articles.
        summarize: Whether to summarize the articles.
        translator: Translator class or the path of it.
        concurrency: Number of concurrent executions.
            Only used when ``translator`` supports async calls.
        timeout: Timeout per article in seconds.
            Only used when ``translator`` supports async calls.
        **options: Other options for ``translator`` (if any).

    Returns:
        Translated (and summarized) articles.

    """
    Translator_: type[Translator]

    if isinstance(translator, str):
        module, name = translator.rsplit(PATH_SEP, PATH_SPLIT)
        Translator_ = getattr(import_module(module), name)
    else:
        Translator_ = translator

    return amap(
        Translator_(language, summarize, **options),
        articles,
        concurrency=concurrency,
        timeout=timeout,
    )


@dataclass
class Translator(ABC):
    """Abstract base class for translators."""

    language: str
    summarize: bool

    def __post_init__(self) -> None:
        """Auto-set translation language from the locale."""
        if self.language == LANG_AUTO:
            locale = Locale.default()
            self.language = str(locale.get_language_name(LANG_EN))

    @abstractmethod
    def __call__(self, article: TArticle, /) -> TArticle:
        """Translate (and summarize) an article."""
        pass

