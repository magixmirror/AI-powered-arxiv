__all__ = ["OpenAI"]


# standard library
from dataclasses import dataclass, replace
from logging import getLogger
from time import sleep


# dependencies
from babel import Locale
from ..article import TArticle
from ..translate import Translator


# constants
LANG_EN = "en"
LOGGER = getLogger(__name__)
PROMPT_TRANSLATE = "Strictly translate the following texts in {language}."
PROMPT_SUMMARIZE = "Summarize the following texts in {language}."


@dataclass
class OpenAI(Translator):
    """Translator by OpenAI generative models.

    Args:
        api_key: API key of the translator.
        language: Language code of the translated articles.
        summarize: Whether to summarize the articles.
        latency: Latency to avoid exceeding the API rate limit.
        model: Name of the generative model.

    """

    latency: float = 1.0
    """Latency to avoid exceeding the API rate limit."""

    model: str = "gpt-3.5-turbo"
    """Name of the generative model."""

    async def __call__(self, article: TArticle, /) -> TArticle:
        """Translate (and summarize) an article."""
        # lazy import
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.api_key)

        # create prompt w/o texts
        language = Locale.parse(self.language).get_language_name(LANG_EN)

        if self.summarize:
            prompt = PROMPT_SUMMARIZE.format(language=language)
        else:
            prompt = PROMPT_TRANSLATE.format(language=language)

        # run translations
        async def run(prompt: str) -> str:
            sleep(self.latency)  # sync sleep!
            completion = await client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return completion.choices[0].text  # type: ignore

        try:
            return replace(
                article,
                title=await run(f"{prompt}\n{article.title}"),
                summary=await run(f"{prompt}\n{article.summary}"),
            )
        except Exception as error:
            LOGGER.warning(error)
            LOGGER.warning(
                f"Failed to translate {article:100}. "
                "The original article was returned instead."
            )
            return article
