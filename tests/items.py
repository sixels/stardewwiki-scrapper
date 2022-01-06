# from src.items import Items

from tests.utils import make_soup

from scrapper.wiki.items import Item


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
}


def test_get_generic_item():
    soup = make_soup("Dark_Sword.html")

    name = Item.page_name(soup)
    assert name and name == DARK_SWORD["name"]

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

    pass
