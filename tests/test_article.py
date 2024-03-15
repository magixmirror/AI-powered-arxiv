# standard library
from asyncio import sleep as async_sleep
from dataclasses import replace
from time import sleep


# dependencies
from aixiv.article import Article, TArticle, amap


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


async def upper(article: TArticle) -> TArticle:
    sleep(1)

    return replace(
        article,
        title=article.title.upper(),
        summary=article.summary.upper(),
    )


async def async_upper(article: TArticle) -> TArticle:
    await async_sleep(1)

    return replace(
        article,
        title=article.title.upper(),
        summary=article.summary.upper(),
    )


def test_amap_sync() -> None:
    assert amap(upper, articles) == articles_upper


def test_amap_async() -> None:
    assert amap(async_upper, articles, timeout=10.0) == articles_upper


def test_amap_async_timeout() -> None:
    assert amap(async_upper, articles, timeout=0.1) == articles
