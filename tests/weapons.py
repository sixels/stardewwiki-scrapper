from src.weapons import Weapons

from tests.utils import make_soup

def test_weapon_stats():
    soup = make_soup("weapons.html")

    stats = Weapons.get_stats(soup)

    print(f"{stats=}")
    assert len(stats) > 0


def test_get_weapons():
    soup = make_soup("weapons.html")

    weapons = Weapons.get_weapons(soup)

    assert len(weapons) > 0
    assert weapons["sword"] is not None
    assert weapons["dagger"] is not None
    assert weapons["club"] is not None
    assert weapons["slingshot"] is not None

