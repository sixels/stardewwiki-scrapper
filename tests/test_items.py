from tests.utils import make_soup

from scrapper.models import Model
from scrapper.models.item import Weapon

DARK_SWORD = {
    "name": "Dark Sword",
    "descriptions": [
        "The Dark Sword is a sword weapon that can be obtained as a Monster drop from Haunted Skulls in the Quarry Mine or dungeon levels in The Mines.",
        "The Dark Sword comes with the vampiric enchantment when obtained from Haunted Skulls. The enchantment can be changed at the Forge.",
    ],
    "notes": [
        "Damage dealt by explosions may also trigger healing as long as the Dark Sword is held. This includes the 999 damage inflicted upon downed Mummies by explosions.",
        "It has the slowest speed and highest weight of any sword in the game.",
    ],
    "details": "It's glowing with vampire energy.",
    "type": "Sword",
    "level": 9,
    "source": "Haunted Skull drop",
    "damage": "30-45",
    "critical_strike_chance": ".04",
    "stats": {"speed": "-5", "crit. chance": "+2", "weight": "+5", "vampiric": "9%"},
    "purchase_price": None,
    "sell_price": 450,
}

RUSTY_SWORD = {
    "name": "Rusty Sword",
    "descriptions": [
        "The Rusty Sword is a sword weapon obtained from Marlon in a cutscene the first time you enter the The Mines."
    ],
    "notes": [],
    "details": "A rusty, dull old sword.",
    "type": "Sword",
    "level": 1,
    "source": "Given by Marlon at the entrance to The Mines",
    "damage": "2-5",
    "critical_strike_chance": ".02",
    "stats": None,
    "purchase_price": None,
    "sell_price": 50,
}


def test_get_item_model():
    soup = make_soup("Dark_Sword.html")

    name = Model.page_name(soup)
    assert name and name == DARK_SWORD["name"]
    assert name == Weapon.page_name(soup)

    descriptions = Model.page_descriptions(soup)
    assert len(descriptions) == len(DARK_SWORD["descriptions"])
    for (current, expected) in zip(descriptions, DARK_SWORD["descriptions"]):
        assert current == expected

    notes = Model.page_notes(soup)
    assert len(notes) == len(DARK_SWORD["notes"])
    for (current, expected) in zip(notes, DARK_SWORD["notes"]):
        assert str(current) == str(expected)


def test_get_darksword_info():
    soup = make_soup("Dark_Sword.html")
    weapon = Weapon.from_page(soup)

    assert len(weapon.info) == len(DARK_SWORD)
    for key in weapon.info.keys():
        assert str(weapon.info[key]) == str(DARK_SWORD[key])


def test_get_rustysword_info():
    soup = make_soup("Rusty_Sword.html")
    weapon = Weapon.from_page(soup)

    assert len(weapon.info) == len(RUSTY_SWORD)
    for key in weapon.info.keys():
        assert str(weapon.info[key]) == str(RUSTY_SWORD[key])
