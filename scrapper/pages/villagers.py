from typing import List

from bs4 import BeautifulSoup

from scrapper.utils import strip_text
from .page import Page


class Villagers(Page):
    @staticmethod
    def page_uri():
        return "/Villagers"

    @staticmethod
    def get_pages(soup: BeautifulSoup) -> List[str]:
        """Get all Villagers url from /Villagers"""

        categories = [
            "Bachelors",
            "Bachelorettes",
            "Non-marriage_candidates",
            "Non-giftable_NPCs",
        ]
        urls = [
            uri
            for uris in [
                get_category_villagers(soup, category) for category in categories
            ]
            for uri in uris
        ]

        return urls


def get_category_villagers(soup: BeautifulSoup, category: str) -> List[str]:
    """Get all villagers from a category"""
    cat_heading = soup.find(id=category)

    assert cat_heading is not None, f"Could not find villager category '{category}'"

    gallery = [
        gallery.find_all("li")
        for gallery in [
            heading.find_next("ul") for heading in soup.find(id=category) if heading
        ]
    ]
    urls = [
        t[1]["href"]
        for t in [row.find_all("a") for rows in gallery for row in rows]
        if len(t) >= 1
    ]

    print (urls)

    return urls
