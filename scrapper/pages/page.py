from typing import List

from bs4 import BeautifulSoup

from .url import make_wiki_url
from scrapper.utils import req_cached, make_soup
from scrapper.models import Model


class Page:
    @staticmethod
    def page_uri() -> str:
        """Returns the relative location of the page on the wiki"""
        raise NotImplementedError()

    @classmethod
    def request_wiki(cls) -> BeautifulSoup:
        """Request and return a parsed wiki page"""
        res = req_cached(make_wiki_url(cls.page_uri()))
        return BeautifulSoup(res, "html.parser")

    @staticmethod
    def get_pages(page: BeautifulSoup):
        """Get relevant wiki pages from this page"""
        raise NotImplementedError()

    @staticmethod
    def model() -> Model:
        """Return the model constructor"""
        raise NotImplementedError()

    @classmethod
    def get_models(cls) -> List[Model]:
        """Get all models from the page"""
        model = cls.model()
        pages = cls.get_pages(cls.request_wiki())

        soups = [make_soup(req_cached(page)) for page in pages]
        return [model.parse(soup) for soup in soups]