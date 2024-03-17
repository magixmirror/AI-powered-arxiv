__all__ = ["Translator", "translate"]


# standard library
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass, field
from importlib import import_module
from logging import getLogger
from os import environ
from re import compile
from typing import Any, Union


# dependencies
from babel import Locale
from .article import Finally, TArticle, amap
from .defaults import (
    API_KEY,
    CONCURRENCY,
    LANGUAGE,
    SUMMARIZE,
    TIMEOUT,
    TRANSLATOR,
)

# type hints
TranslatorLike = Union[type["Translator"], str]


# constants
ENV_PATTERN = compile(r"^\$\{{0,1}(.+?)\}{0,1}$")
LANG_AUTO = "auto"
LANG_EN = "en"
LOGGER = getLogger(__name__)
PATH_SEP = "."
PATH_SPLIT = 1


@dataclass
class Translator(ABC):
    """Abstract base class for translators.

    Args:
        api_key: API key or the environment variable for it.
        language: Language code of the translated articles.
        summarize: Whether to summarize the articles.

    """

    api_key: str = field(repr=False)
    """API key or the environment variable for it."""

    language: str
    """Language code of the translated articles."""

    summarize: bool
    """Whether to summarize the articles."""

    @abstractmethod
    def __call__(self, article: TArticle, /) -> Finally[TArticle]:
        """Translate (and summarize) an article."""
        pass


def translate(
    articles: Iterable[TArticle],
    /,
    *,
    # options for translator
    translator: TranslatorLike = TRANSLATOR,
    api_key: str = API_KEY,
    language: str = LANGUAGE,
    summarize: bool = SUMMARIZE,
    # options for mapping
    concurrency: int = CONCURRENCY,
    timeout: float = TIMEOUT,
    # other options for translator
    **options: Any,
) -> list[TArticle]:
    """Translate (and summarize) articles.

    Args:
        articles: Articles to be translated.
        translator: Translator class or the path for it.
        api_key: API key of the translator or the environment
            variable for it. The latter must start with ``"$"``.
        language: Language code of the translated articles.
            If it is ``"auto"``, the locale language will be used.
        summarize: Whether to summarize the articles.
        concurrency: Number of concurrent executions.
            Only used when ``translator`` supports async calls.
        timeout: Timeout per article in seconds.
            Only used when ``translator`` supports async calls.
        **options: Other options for ``translator`` (if any).

    Returns:
        Translated (and summarized) articles.

    """
    # parse translator
    Translator_: type[Translator]

    if isinstance(translator, str):
        module, name = translator.rsplit(PATH_SEP, PATH_SPLIT)
        Translator_ = getattr(import_module(module), name)
    else:
        Translator_ = translator

    # parse API key
    if match := ENV_PATTERN.search(api_key):
        api_key = environ[match[1]]

    # parse language
    if language == LANG_AUTO:
        locale = Locale.default()
    else:
        locale = Locale.parse(language)

    language = str(locale.get_language_name(LANG_EN))

    return amap(
        Translator_(api_key, language, summarize, **options),
        articles,
        concurrency=concurrency,
        timeout=timeout,
    )
