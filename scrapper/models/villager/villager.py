from typing import TypedDict, List, Tuple, Union, Dict

from bs4 import BeautifulSoup

from scrapper.models import Model, ModelInfo
from scrapper.utils import strip_text, normalized_list


class Schedule(TypedDict):
    time: str
    location: str


class Gift(TypedDict):
    name: str
    description: str
    source: Union[List[str], None]
    ingredients: Union[List[str], None]


class VillagerSchedules(TypedDict):
    brief: List[str]
    schedule: Dict[str, List[Tuple[str, List[Schedule]]]]  # [(condition, schedules)]


class VillagerGifts(TypedDict):
    kind: str
    quote: str
    gift: List[Gift]


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
    gifts: Union[List[VillagerGifts], None]


class Villager(Model):
    info: VillagerInfo

    def __init__(self, info: VillagerInfo):
        self.info = info

    @classmethod
    def from_page(cls, page: BeautifulSoup):
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

        # print(villager)
        get_schedules(page)

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
        v = True if v == "Yes" else False

    return (k, v)


def get_quote(page: BeautifulSoup) -> Union[str, None]:
    quote = page.find_all("td", class_="quotetext")
    if quote and quote[0]:
        return strip_text(quote[0]).strip("“”") if quote[0] else ""
    else:
        return None


def get_schedules(page: BeautifulSoup) -> Union[VillagerSchedules, None]:
    schedules_heading = page.find(id="Schedule")
    if schedules_heading is None:
        return None

    briefs_p = schedules_heading.find_all_next()
    brief = []
    for p in briefs_p:
        if p:
            if p.name != "p":
                if len(brief) > 0:
                    break
            else:
                if len((desc := strip_text(p))) > 1:
                    brief += [desc]

    schedules_table = schedules_heading.find_next("table")

    events = []
    while schedules_table.name == "table":
        events += [strip_text(schedules_table.find_next("tr"))]
        schedules_table = schedules_table.find_next_sibling()

    print(brief, events)

    return None
    # return VillagerSchedules(brief=brief)
