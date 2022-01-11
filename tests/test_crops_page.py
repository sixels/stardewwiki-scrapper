from scrapper.pages import Crops

from tests.utils import make_soup

def test_get_weapons():
    soup = make_soup("Crops.html")

    uris = Crops.get_pages(soup)