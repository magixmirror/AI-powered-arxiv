# dependencies
from aixiv.search import search


# constants
CATEGORIES = ("astro-ph.GA",)
KEYWORDS = ("galaxy",)
START = "2021-01-01 in UTC"
END = "2021-01-02 in UTC"
EXPECTED_URLS = [
    "http://arxiv.org/abs/2101.00188v2",
    "http://arxiv.org/abs/2101.00158v1",
    "http://arxiv.org/abs/2101.00253v3",
    "http://arxiv.org/abs/2101.00283v1",
]


# test functions
def test_search() -> None:
    articles = search(CATEGORIES, KEYWORDS, START, END)
    urls = [article.url for article in articles]
    assert urls == EXPECTED_URLS
