__all__ = ["DeepL"]


# standard library
from dataclasses import replace
from functools import partial
from logging import getLogger
from typing import cast


# dependencies
from ..article import TArticle
from ..translate import Translator


# constants
LOGGER = getLogger(__name__)


class DeepL(Translator):
    """Translator by DeepL neural network.

    Args:
        api_key: API key of the translator.
        language: Language code of the translated articles.
        summarize: Whether to summarize the articles.

    """

    def __call__(self, article: TArticle, /) -> TArticle:
        """Translate (and summarize) an article."""
        # lazy import
        from deepl import TextResult, Translator

        model = Translator(self.api_key)
        run = partial(model.translate_text, target_lang=self.language)

        if self.summarize:
            LOGGER.warning("Summarization is not supported by DeepL.")

        try:
            resp_title = cast(TextResult, run(article.title))
            resp_summary = cast(TextResult, run(article.summary))

            return replace(
                article,
                title=resp_title.text,
                summary=resp_summary.text,
            )
        except Exception as error:
            LOGGER.warning(error)
            LOGGER.warning(
                f"Failed to translate {article:100}. "
                "The original article was returned instead."
            )
            return article
