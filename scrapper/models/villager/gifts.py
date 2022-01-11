from typing import Union, List, Tuple, Dict, TypedDict

from bs4 import BeautifulSoup

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
