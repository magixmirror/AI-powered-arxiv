__all__ = ["AsyncTranslator", "Translator"]


# standard library
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import getLogger


# dependencies
from babel import Locale
from .article import TArticle


# constants
LANG_AUTO = "auto"
LANG_EN = "en"
LOGGER = getLogger(__name__)


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


@dataclass
class AsyncTranslator(ABC):
    """Abstract base class for async-translators."""

    language: str
    summarize: bool

    def __post_init__(self) -> None:
        """Auto-set translation language from the locale."""
        if self.language == LANG_AUTO:
            locale = Locale.default()
            self.language = str(locale.get_language_name(LANG_EN))

    @abstractmethod
    async def __call__(self, article: TArticle, /) -> TArticle:
        """Translate (and summarize) an article."""
        pass
