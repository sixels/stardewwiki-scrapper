from typing import TypedDict, List, Tuple, Union, Dict

from bs4 import BeautifulSoup

from scrapper.models import Model, ModelInfo
from scrapper.utils import strip_text, normalized_list


class Schedule(TypedDict):
    time: str
    location: str


class VillagerSchedules(Model):
    brief: List[str]
    schedule: List[
        Tuple[str, List[Tuple[Union[str, None], List[Schedule]]]]
    ]  # [( requirement, [( condition, [schedules] )] )]

    def __init__(
        self,
        brief: List[str],
        schedule: Dict[str, List[Tuple[Union[str, None], List[Schedule]]]],
    ):
        self.brief = brief
        self.schedule = schedule

    @classmethod
    def parse(cls, page: BeautifulSoup):
        schedules_heading = page.find(id="Schedule")
        if schedules_heading is None:
            return None

        briefs_p = schedules_heading.find_all_next()
        is_special = briefs_p[0].name == "h3"

        brief = []
        if not is_special:
            for p in briefs_p:
                if p.name != "p":
                    if len(brief) > 0 or p.name == "h2":
                        break
                else:
                    if len((desc := strip_text(p))) > 1:
                        brief += [desc]

        schedule_tables = schedules_heading.find_all_next(["table", "h2"])

        schedules = {"requirement": None, "schedules": []}
        vschedule = []
        for sched_elm in schedule_tables:
            if sched_elm.name == "h2":
                vschedule += [(schedules["requirement"], schedules["schedules"])]
                break
            if sched_elm.name == "table":
                if (c_ := sched_elm.get("class")) and "wikitable" in c_:
                    if not is_special:
                        condition = (
                            strip_text(c)
                            if (
                                c := sched_elm.find_previous_siblings(["p", "h2"])[0]
                            ).name
                            == "p"
                            else strip_text(sched_elm.find_next("th"))
                        )
                        requirement = (
                            strip_text(r)
                            if not (r := sched_elm.find_previous("span")).get("class")
                            else None
                        )
                    else:
                        condition = strip_text(sched_elm.find_next("th"))
                        requirement = (
                            strip_text(r)
                            if (r := sched_elm.find_previous("h3"))
                            else None
                        )

                    rows = sched_elm.find_all("tr")[1:]
                    schedule = [
                        Schedule(time=col[0], location=col[1])
                        for col in [
                            (strip_text(cols[0]), strip_text(cols[1]))
                            for cols in [row.find_all("td") for row in rows]
                        ]
                    ]
                    schedules["requirement"] = requirement
                    schedules["schedules"] += [(condition, schedule)]
                else:
                    if len(schedules["schedules"]):
                        vschedule += [
                            (schedules["requirement"], schedules["schedules"])
                        ]
                        schedules["schedules"] = []

                    is_special = False

        return cls(brief=brief, schedule=vschedule)


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
