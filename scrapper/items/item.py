from bs4 import BeautifulSoup

from scrapper.utils import strip_text


class Item:
    @staticmethod
    def page_name(page: BeautifulSoup) -> str or None:
        heading = page.find(id="firstHeading")
        return None if heading is None else strip_text(heading)

    @staticmethod
    def page_descriptions(page: BeautifulSoup) -> [str]:
        desc_p = page.find(id="infoboxborder")
        if not desc_p:
            return None

        desc_p = desc_p.find_next_siblings()

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
    def page_notes(page: BeautifulSoup) -> [str]:
        notes_div = page.find(id="Notes")

        notes = []
        if notes_div is not None:
            notes_list = notes_div.find_next("ul")
            if notes_list is not None:
                notes_ = notes_list.find_all("li")
                for note in notes_:
                    notes += [strip_text(note)]

        return notes

    @classmethod
    def from_page(cls, page: BeautifulSoup):
        """Create an item from the wiki page and return it"""
        pass
