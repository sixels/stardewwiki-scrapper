from typing import List, Union

from bs4 import BeautifulSoup

from scrapper.models import Model, ModelInfo
from scrapper.utils import strip_text, normalized_list
from .schedules import VillagerSchedules
from .gifts import VillagerGifts


class VillagerInfo(ModelInfo):
    """A generic villager information"""

    quote: Union[str, None]

    birthday: str
    lives_in: str
    address: List[str]
    family: List[str]
    friends: List[str]
    marriage: bool

    schedules: Union[VillagerSchedules, None]
    gifts: Union[VillagerGifts, None]

    # TODO: Parse Quests and Shop sections


class Villager(Model):
    info: VillagerInfo

    def __init__(self, info: VillagerInfo):
        self.info = info

    @classmethod
    def parse(cls, page: BeautifulSoup):
        villager = VillagerInfo()

        villager["name"] = Model.page_name(page)
        villager["descriptions"] = Model.page_descriptions(page)
        villager["notes"] = Model.page_notes(page)
        villager["quote"] = get_quote(page)

        # parse the villager's info box
        info_box = page.find(id="infoboxtable")
        assert info_box is not None, "Could not find any #infoboxtable on page"

        rows = info_box.find_all("tr")[2:]  # skip the villager name and image
        info_table = dict(
            parse_key_val(key, val)
            for key in (row.find_next("td") for row in rows[:-1])
            if key["id"] == "infoboxsection" and (val := key.find_next_sibling())
        )
        villager.update(info_table)
        villager["schedules"] = VillagerSchedules.parse(page)
        villager["gifts"] = VillagerGifts.parse(page)

        return cls(villager)


def parse_key_val(key, val) -> (str, Union[str, int, dict, None]):
    """Parse the fields from the info table with the right types"""

    k = strip_text(key)[:-1].lower().replace(" ", "_")
    v = strip_text(val)

    if "address" in k:
        v = [s.replace(" )", " ❤️)") for s in normalized_list(v)]
    if "friends" in k:
        v = [s for s in v.split(" ") if len(s)]
    if "family" in k:
        v = normalized_list(v)
    if "marriage" in k:
        v = "Yes" in v

    return (k, v)


def get_quote(page: BeautifulSoup) -> Union[str, None]:
    quote = page.find_all("td", class_="quotetext")
    if quote and quote[0]:
        return strip_text(quote[0]).strip("“”") if quote[0] else ""
    else:
        return None
