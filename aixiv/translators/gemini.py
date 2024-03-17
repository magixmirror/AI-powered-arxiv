__all__ = ["Gemini"]


# standard library
from dataclasses import replace
from logging import getLogger


# dependencies
from ..article import TArticle
from ..translate import Translator


# constants
LOGGER = getLogger(__name__)
PROMPT_TRANSLATE = "Strictly translate the following texts in {gemini.language}."
PROMPT_SUMMARIZE = "Summarize the following texts in {gemini.language}."


class Gemini(Translator):
    """Google/Gemini translator.

    Args:
        api_key: API key of the translator.
        language: Language code of the translated articles.
        summarize: Whether to summarize the articles.
        model: Name of the generative model.

    """

    model: str = "gemini-pro"
    """Name of the generative model."""

    async def __call__(self, article: TArticle, /) -> TArticle:
        """Translate (and summarize) an article."""
        # lazy import
        from google import generativeai as genai

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)
        run = model.generate_content_async

        if self.summarize:
            prompt = PROMPT_SUMMARIZE.format(gemini=self)
        else:
            prompt = PROMPT_TRANSLATE.format(gemini=self)

        try:
            resp_title = await run(f"{prompt}\n{article.title}")
            resp_summary = await run(f"{prompt}\n{article.summary}")

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
