__all__ = ["DeepL"]


# standard library
from dataclasses import dataclass, replace
from logging import getLogger
from typing import cast


# dependencies
from ..article import TArticle
from ..translate import Translator


# constants
LOGGER = getLogger(__name__)


@dataclass
class DeepL(Translator):
    """Translator by DeepL neural network.

    Args:
        api_key: API key of the translator.
        language: Language code of the translated articles.
        summarize: Whether to summarize the articles.

    """

    def __post_init__(self) -> None:
        if self.summarize:
            LOGGER.warning("Summarization is not supported.")

    def __call__(self, article: TArticle, /) -> TArticle:
        """Translate (and summarize) an article."""
        # create model
        from deepl import TextResult, Translator

        model = Translator(self.api_key)

        # run translations
        def run(prompt: str) -> str:
            response = model.translate_text(
                text=prompt,
                target_lang=self.language,
            )
            return cast(TextResult, response).text

        try:
            return replace(
                article,
                title=run(article.title),
                summary=run(article.summary),
            )
        except Exception as error:
            LOGGER.warning(error)
            LOGGER.warning(
                f"Failed to translate {article:100}. "
                "The original article was returned instead."
            )
            return article
