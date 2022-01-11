# from src.items import Items

from tests.utils import make_soup

from scrapper.models import Model
from scrapper.models.villager import Villager

HALEY = {
    "name": "Haley",
    "descriptions": [
        "Haley is a villager who lives in Pelican Town. She's one of the twelve characters available to marry."
    ],
    "notes": [],
    "birthday": "Spring 14",
    "lives_in": "Pelican Town",
    "address": ["2 Willow Lane"],
    "family": ["Emily (Sister)"],
    "friends": ["Alex"],
    "marriage": True,
    "schedules": {
        "brief": [
            "Her behavior changes if it's raining or snowing outside. She will not go to the fountain Tuesday-Sunday if it is raining.",
            "Her house is usually unlocked from 9am to 8pm. If she is inside when it is locked and you are not, she will be inaccessible to you.",
        ],
        "schedule": [
            (
                "Spring",
                [
                    (
                        "Monday",
                        [
                            {
                                "location": "In her room",
                                "time": "9:00 AM",
                            },
                            {
                                "location": "Leaves her room to go to kitchen",
                                "time": "10:00 AM",
                            },
                            {
                                "location": "Leaving home to go to the river south of Marnie's Ranch",
                                "time": "11:00 AM",
                            },
                            {
                                "location": "By the river south of Marnie's Ranch, taking pictures",
                                "time": "12:20 PM",
                            },
                            {
                                "location": "Heads home",
                                "time": "4:30 PM",
                            },
                            {
                                "location": "At home, cooking dinner",
                                "time": "5:50 PM",
                            },
                            {
                                "time": "8:20 PM",
                                "location": "In her room",
                            },
                            {
                                "time": "11:00 PM",
                                "location": "Goes to bed",
                            },
                        ],
                    ),
                ],
            )
        ],
    },
    "gifts": {
        "gift": [
            {
                "love": (
                    ["Oh my god, this is my favorite thing!"],
                    [
                        ["All Universal Loves (except Prismatic Shard)"],
                        {
                            "name": "Coconut",
                            "description": "A seed of the coconut palm. It has many culinary uses.",
                            "source": ["Foraging"],
                            "ingredients": None,
                        },
                        {
                            "name": "Fruit Salad",
                            "description": "A delicious combination of summer fruits.",
                            "source": ["Cooking"],
                            "ingredients": [
                                "Blueberry (1)",
                                "Melon (1)",
                                "Apricot (1)",
                            ],
                        },
                        {
                            "name": "Pink Cake",
                            "description": "There's little heart candies on top.",
                            "source": ["Cooking"],
                            "ingredients": [
                                "Melon (1)",
                                "Wheat Flour (1)",
                                "Sugar (1)",
                                "Egg (1)",
                            ],
                        },
                        {
                            "name": "Sunflower",
                            "description": "A common misconception is that the flower turns so it's always facing the sun.",
                            "source": ["Farming"],
                            "ingredients": None,
                        },
                    ],
                )
            }
        ]
    },
}


def test_get_villager_model():
    soup = make_soup("Haley.html")

    name = Model.page_name(soup)
    assert name == HALEY["name"]

    descriptions = Model.page_descriptions(soup)
    assert descriptions == HALEY["descriptions"]

    notes = Model.page_notes(soup)
    assert notes == HALEY["notes"]


def test_get_haley_info():
    soup = make_soup("Haley.html")

    haley = Villager.parse(soup)

    assert haley.info["birthday"] == HALEY["birthday"]
    assert haley.info["address"] == HALEY["address"]
    assert haley.info["lives_in"] == HALEY["lives_in"]
    assert haley.info["family"] == HALEY["family"]
    assert haley.info["friends"] == HALEY["friends"]
    assert haley.info["marriage"] == HALEY["marriage"]

    assert haley.info["schedules"].brief == HALEY["schedules"]["brief"]
    # print(haley.info["schedules"].schedule[0])
    assert (
        haley.info["schedules"].schedule[0][0] == HALEY["schedules"]["schedule"][0][0]
    )
    for (c, e) in zip(
        haley.info["schedules"].schedule[0][1], HALEY["schedules"]["schedule"][0][1]
    ):
        assert c[0] == e[0]
        for (sc, se) in zip(c[1], e[1]):
            assert sc["time"] == se["time"] and sc["location"] == se["location"]

    current_gift = haley.info["gifts"].gift[0]
    expected_gift = HALEY["gifts"]["gift"][0]

    # quotes
    for (c, e) in zip(current_gift["love"][0], expected_gift["love"][0]):
        assert c == e
    # gifts
    for (c, e) in zip(current_gift["love"][1], expected_gift["love"][1]):
        for (cc, ee) in zip(c, e):
            assert cc == ee


def test_get_leo_info():
    soup = make_soup("Leo.html")

    leo = Villager.parse(soup)
    assert leo is not None
