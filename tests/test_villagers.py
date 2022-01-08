# from src.items import Items

from tests.utils import make_soup

from scrapper.models import Model
from scrapper.models.villager import Villager

HALEY = {
    "name": "Haley",
    "descriptions": [
        "Haley is a villager who lives in Pelican Town. She's one of the twelve characters available to marry."
    ],
    "notes": []
}


def test_get_villager_model():
    soup = make_soup("Haley.html")

    name = Model.page_name(soup)
    assert name and name == HALEY.name

    descriptions = Model.page_descriptions(soup)
    assert descriptions == HALEY.descriptions

    notes = Model.page_notes(soup)
    assert notes == HALEY.notes

def test_get_haley_info():
    pass