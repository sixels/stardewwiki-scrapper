# from src.items import Items

from tests.utils import make_soup

from scrapper.items import Item, Weapon

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


def test_get_generic_item_info():
    soup = make_soup("Dark_Sword.html")

    name = Item.page_name(soup)
    assert name and name == DARK_SWORD["name"]
    assert name == Weapon.page_name(soup)

    descriptions = Item.page_descriptions(soup)
    assert len(descriptions) == len(DARK_SWORD["descriptions"])
    for (current, expected) in zip(descriptions, DARK_SWORD["descriptions"]):
        assert current == expected

    notes = Item.page_notes(soup)
    assert len(notes) == len(DARK_SWORD["notes"])
    for (current, expected) in zip(notes, DARK_SWORD["notes"]):
        assert current == expected


def test_get_weapon_info():
    soup = make_soup("Dark_Sword.html")
    weapon = Weapon.from_page(soup)

    assert len(weapon.info) == len(DARK_SWORD)
    for (current, expected) in zip(weapon.info.values(), DARK_SWORD.values()):
        assert str(current) == str(expected)
