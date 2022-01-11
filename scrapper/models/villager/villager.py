from typing import TypedDict, List, Tuple, Union, Dict

from bs4 import BeautifulSoup

from scrapper.models import Model, ModelInfo
from scrapper.utils import strip_text, normalized_list
from .schedules import VillagerSchedules


class VillagerGifts(Model):
    Gift = Union[
        TypedDict(
            "NormalGift",
            {
                "name": str,
                "description": str,
                "source": Union[List[str], None],
                "ingredients": Union[List[str], None],
            },
        ),
        List[str],
    ]

    gift: List[
        Dict[
            str,
            Tuple[
                List[str],
                List[Gift],
            ],
        ]
    ]  # [{love|like|neutral|dislike|hate: ([quotes], [gifts])}]

    def __init__(self, gifts):
        self.gift = gifts

    @classmethod
    def parse(cls, page: BeautifulSoup):
        gifts_heading = page.find(id="Gifts")
        if gifts_heading is None:
            return None

        headlines = gifts_heading.find_all_next(class_="mw-headline")
        gift = []
        for headline in headlines:
            if headline.parent.name != "h3":
                break

            tables = headline.find_all_next("table")

            quotes, gifts = [], []
            for table in tables:
                if table.get("class") is not None:
                    rows = table.find_all("tr")
                    columns = [strip_text(col) for col in rows[0].find_all("th")[1:]]

                    # print(columns)
                    gifts += [
                        [strip_text(item) for item in col.find_all("li")]
                        if len(cols) == 2
                        else dict(
                            map(
                                parse_gift_key_val,
                                zip(columns, cols[1:]),
                            )
                        )
                        for cols in [row.find_all("td") for row in rows[1:]]
                        for col in cols[1:]
                    ]

                    break
                quotes += [strip_text(table.find_next(class_="quotetext")).strip("“”")]
            gift += [{strip_text(headline).lower().replace(" ", "_"): (quotes, gifts)}]
        return cls(gift)


def parse_gift_key_val(tup):
    k = tup[0].lower()
    v = strip_text(tup[1])

    if "ingredients" in k:
        v = [s for s in normalized_list(v) if len(s)] or None
    if "source" in k:
        v = [s.strip() for s in v.split("-") if len(s) > 2] or None

    return (k, v)


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
