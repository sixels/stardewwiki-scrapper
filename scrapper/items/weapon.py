from typing import TypedDict

from bs4 import BeautifulSoup

from scrapper.utils import strip_text, normalized_stats
from scrapper.items import Item


class WeaponInfo(TypedDict):
    """item name"""

    name: str
    """item description"""
    descriptions: [str]
    """item notes"""
    notes: [str]
    """in-game description text"""
    detail: str

    """the weapon type (sword, dagger, ...)"""
    type_: str
    level: str
    damage: str
    critical_strike_chance: str
    """weapon stats (speed, defense, ...)"""
    stats: str or None
    """where it can be obtained"""
    source: str
    purchase_price: int or None
    sell_price: int or None


class Weapon(Item):
    info: WeaponInfo

    def __init__(self, info: WeaponInfo):
        self.info = info

    @classmethod
    def from_page(cls, page: BeautifulSoup):
        name = Item.page_name(page)
        descriptions = Item.page_descriptions(page)
        notes = Item.page_notes(page)

        info_box = soup.find(id="infoboxtable")
        if info_box is None:
            print("Could not find the info box")
            return infos

        rows = info_box.find_all("tr")[2:]

        detail = strip_text(rows[0].find_next(id="infoboxdetail"))

        section = None
        for row in rows[1:]:
            col = row.find_next("td")

            if col["id"] == "infoboxsection":
                col_val = col.find_next_sibling()
                if col_val is None:
                    section = strip_text(col)
                    aditional[section] = {}
                else:
                    # the last character is a colon
                    key = strip_text(col)[:-1]

                    value = (
                        strip_text(col_val)
                        if key != "Stats"
                        else normalized_stats(col_val)
                    )

                    if section is not None:
                        aditional[section][key] = value
                    else:
                        aditional[key] = value

        aditional["details"] = details
        infos["aditional"] = aditional
        return infos
