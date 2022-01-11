from typing import List, Tuple, Union, Generator

from bs4 import BeautifulSoup

from .page import Page


class Crops(Page):
    @staticmethod
    def page_uri():
        return "/Villagers"

    @staticmethod
    def model():
        from scrapper.models.crop import Crop

        return Crop

    @staticmethod
    def get_pages(page: BeautifulSoup) -> List[Generator]:
        categories = ["Spring_Crops", "Summer_Crops", "Fall_Crops", "Special_Crops"]
        return [get_category_crops(page, category) for category in categories]


def get_category_crops(
    page: BeautifulSoup, category: str
) -> List[Tuple[Union[str, None], str]]:
    cat_heading = page.find(id=category)

    assert cat_heading is not None, f"Could not find crop category: '{category}'"

    crops_heading = cat_heading.find_all_next(["h3", "h2"])
    for heading in crops_heading:
        if heading.name == "h2":
            break
        try:
            crop = heading.find_all("a")[1]

            if crop["title"] == "Mixed Seeds":
                yield (None, crop["href"])
            else:
                yield (
                    crop["href"],
                    heading.find_next("table")
                    .find_next(class_="center")
                    .find_next_sibling("a")["href"],
                )

        except IndexError:
            pass
