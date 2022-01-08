from typing import TypedDict, List, Tuple, Union

from bs4 import BeautifulSoup

from scrapper.models import Model
from scrapper.utils import strip_text


class Schedule(TypedDict):
    time: str
    location: str


class Gift(TypedDict):
    name: str
    description: str
    source: Union[List[str], None]
    ingredients: Union[List[str], None]


class VillagerSchedule(TypedDict):
    season: str
    schedule: List[Tuple[str, Schedule]]  # (condition, schedule)


class VillagerGifts(TypedDict):
    kind: str
    quote: str
    Gift


class VillagerInfo(TypedDict):
    """A generic villager information"""

    name: str
    quote: Union[str, None]
    descriptions: List[str]

    birthday: str
    lives_in: str
    address: str
    friends: List[str]
    marriage: bool

    schedule: Union[List[VillagerSchedule], None]
    gifts: Union[List[VillagerGifts], None]


class Villager(Model):
    from scrapper.models import Model

    info: VillagerInfo
