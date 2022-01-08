from typing import TypedDict, Union

from bs4 import BeautifulSoup

from scrapper.utils import strip_text, normalized_stats
from scrapper.models import Model
from .item import ItemInfo


class WeaponInfo(ItemInfo):
    """A Weapon information"""

    """In-game description text"""
    details: str
    """Weapon type (sword, dagger, ...)"""
    type_: str
    level: str
    damage: str
    critical_strike_chance: str
    """Weapon stats (speed, defense, ...)"""
    stats: str or None
    """Where it can be obtained"""
    source: str
    purchase_price: int or None
    sell_price: int or None


class Weapon(Model):
    info: WeaponInfo

    def __init__(self, info: WeaponInfo):
        self.info = info

    @classmethod
    def from_page(cls, page: BeautifulSoup):
        weapon = WeaponInfo()

        weapon["name"] = Model.page_name(page)
        weapon["descriptions"] = Model.page_descriptions(page)
        weapon["notes"] = Model.page_notes(page)

        info_box = page.find(id="infoboxtable")
        assert info_box is not None, "Could not find any #infoboxtable on page"

        # get the in-game description
        rows = info_box.find_all("tr")[2:]  # skip the weapon name and image
        weapon["details"] = strip_text(rows[0].find_next(id="infoboxdetail"))

        weapon["stats"] = None
        # parse the rest of the table
        table = dict(
            parse_key_val(key, val)
            for key in (row.find_next("td") for row in rows[1:])
            if key["id"] == "infoboxsection" and (val := key.find_next_sibling())
        )
        weapon.update(table)

        return cls(info=weapon)


def parse_key_val(key, val) -> (str, Union[str, int, dict, None]):
    """Parse the fields from the info table with the right types"""

    k = strip_text(key)[:-1].lower().replace(" ", "_")
    v = strip_text(val)
    if "price" in k:
        v = int_or_none(v[:-1])
    elif "level" in k:
        v = int_or_none(v)
    elif "stats" in k:
        v = normalized_stats(v)

    return (k, v)


def int_or_none(s: str) -> int or None:
    import re

    digits = re.search(r"\d+", s)
    return int(digits.group()) if digits else None
