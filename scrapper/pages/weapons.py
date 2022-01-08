from typing import List

from bs4 import BeautifulSoup

from scrapper.utils import strip_text
from .page import Page


class Weapons(Page):
    @staticmethod
    def page_uri():
        return "/Weapons"

    @staticmethod
    def get_pages(soup: BeautifulSoup) -> List[str]:
        """Get all weapons url from /Weapons"""

        categories = [
            "Sword",
            "Dagger",
            "Club",
            "Slingshot",
            "Unobtainable_Weapons",
        ]
        urls = [
            uri
            for uris in [
                get_category_weapons(soup, category) for category in categories
            ]
            for uri in uris
        ]

        return urls


def get_category_weapons(soup: BeautifulSoup, category: str) -> List[str]:
    """Get all weapons from a category"""
    cat_heading = soup.find(id=category)

    assert cat_heading is not None, f"Could not find weapon category '{category}'"

    table = [
        table.find_all("tr")
        for table in [
            heading.find_next("tbody") for heading in soup.find(id=category) if heading
        ]
    ]
    urls = [
        t[1]["href"]
        for t in [row.find_all("a") for rows in table for row in rows]
        if len(t) >= 1
    ]

    return urls
