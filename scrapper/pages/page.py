from bs4 import BeautifulSoup

from .url import make_wiki_url
from scrapper.utils import req_cached


class Page:
    @staticmethod
    def page_uri() -> str:
        """Returns the relative location of the page on the wiki"""
        raise NotImplementedError()

    @classmethod
    def make_soup(cls) -> BeautifulSoup:
        """Request and return a parsed wiki page"""
        res = req_cached(make_wiki_url(cls.page_uri()))
        return BeautifulSoup(res, "html.parser")
