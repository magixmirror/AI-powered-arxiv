# dependencies
from dataclasses import dataclass, replace
from aixiv.article import Article, TArticle
from aixiv.translate import Translator, translate


# test datasets
articles = [
    Article("Title A", ["Author A"], "Summary A", "http://example.com/a"),
    Article("Title B", ["Author B"], "Summary B", "http://example.com/b"),
    Article("Title C", ["Author C"], "Summary C", "http://example.com/c"),
]
articles_upper = [
    Article("TITLE A", ["Author A"], "SUMMARY A", "http://example.com/a", articles[0]),
    Article("TITLE B", ["Author B"], "SUMMARY B", "http://example.com/b", articles[1]),
    Article("TITLE C", ["Author C"], "SUMMARY C", "http://example.com/c", articles[2]),
]


@dataclass
class Tester(Translator):
    def __call__(self, article: TArticle, /) -> TArticle:
        return replace(
            article,
            title=article.title.upper(),
            summary=article.summary.upper(),
        )


@dataclass
class AsyncTester(Translator):
    async def __call__(self, article: TArticle, /) -> TArticle:
        return replace(
            article,
            title=article.title.upper(),
            summary=article.summary.upper(),
        )


# test functions
def test_translate() -> None:
    assert translate(articles, translator=Tester) == articles_upper


def test_translate_async() -> None:
    assert translate(articles, translator=AsyncTester) == articles_upper
