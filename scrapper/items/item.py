from typing import TypedDict

from bs4 import BeautifulSoup

from scrapper.utils import strip_text


class ItemInfo(TypedDict):
    """A generic item information"""

    """Item name"""
    name: str
    """Item descriptions"""
    descriptions: list[str]
    """Item notes"""
    notes: list[str]


class Item:
    @staticmethod
    def page_name(page: BeautifulSoup) -> str or None:
        heading = page.find(id="firstHeading")
        return None if heading is None else strip_text(heading)

    @staticmethod
    def page_descriptions(page: BeautifulSoup) -> list[str]:
        desc_p = page.find(id="infoboxborder")
        if not desc_p:
            return None

        desc_p = desc_p.find_next_siblings()

        # ignore the "spoiler" box
        descriptions = []
        for p in desc_p:
            if p:
                if p.name != "p":
                    if len(descriptions) > 0:
                        break
                else:
                    descriptions += [strip_text(p)]

        return descriptions

    @staticmethod
    def page_notes(page: BeautifulSoup) -> list[str]:
        notes_div = page.find(id="Notes")

        uls = [ul.find_all("li") for ul in [notes_div.find_next("ul")] if ul]
        notes = [strip_text(note) for lis in uls for note in lis]

        return notes

    @classmethod
    def from_page(cls, page: BeautifulSoup):
        """Create an item from the wiki page and return it"""
        raise NotImplementedError()
