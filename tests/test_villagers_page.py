from scrapper.pages import Villagers

from tests.utils import make_soup

def test_get_weapons():
    soup = make_soup("Villagers.html")

    uris = Villagers.get_villagers_uri(soup)