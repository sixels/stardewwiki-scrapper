import pytest

from scrapper.pages import Weapons

from tests.utils import make_soup

URIS = [
    "/Rusty_Sword",
    "/Steel_Smallsword",
    "/Wooden_Blade",
    "/Silver_Saber",
    "/Cutlass",
    "/Forest_Sword",
    "/Iron_Edge",
    "/Insect_Head",
    "/Bone_Sword",
    "/Claymore",
    "/Obsidian_Edge",
    "/Ossified_Blade",
    "/Tempered_Broadsword",
    "/Yeti_Tooth",
    "/Steel_Falchion",
    "/Dark_Sword",
    "/Lava_Katana",
    "/Dragontooth_Cutlass",
    "/Dwarf_Sword",
    "/Galaxy_Sword",
    "/Infinity_Blade",
    "/Carving_Knife",
    "/Iron_Dirk",
    "/Wind_Spire",
    "/Elf_Blade",
    "/Crystal_Dagger",
    "/Shadow_Dagger",
    "/Broken_Trident",
    "/Wicked_Kris",
    "/Galaxy_Dagger",
    "/Dwarf_Dagger",
    "/Dragontooth_Shiv",
    "/Iridium_Needle",
    "/Infinity_Dagger",
    "/Femur",
    "/Wood_Club",
    "/Wood_Mallet",
    "/Lead_Rod",
    "/Kudgel",
    "/The_Slammer",
    "/Galaxy_Hammer",
    "/Dwarf_Hammer",
    "/Dragontooth_Club",
    "/Infinity_Gavel",
    "/Slingshot",
    "/Master_Slingshot",
    "/Holy_Blade",
    "/Rapier",
    "/Galaxy_Slingshot",
    "/Bone_Sword",
    "/Broken_Trident",
    "/Dragontooth_Club",
]


def test_get_weapons():
    soup = make_soup("Weapons.html")

    uris = Weapons.get_pages(soup)
    for uri in URIS:
        assert uri in uris


@pytest.mark.skip(
    reason="This test makes a request to stardewvalleywiki.com, which might slow down the test execution."
)
def test_make_req():
    from scrapper.utils import make_cache_dir

    make_cache_dir()
    soup = Weapons.request_wiki()

    uris = Weapons.get_pages(soup)
    assert len(uris) > 0
