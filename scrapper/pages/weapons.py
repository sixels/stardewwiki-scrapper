class Weapons:
    @staticmethod
    def wiki_uri():
        return "Weapons"

    @staticmethod
    def get_stats(soup: BeautifulSoup) -> dict:
        weapon_stats_heading = soup.find(id="Weapon_Stats")

        if weapon_stats_heading is None:
            print("Could not find Weapon Stats")
            return {}

        table = weapon_stats_heading.find_next("table")
        columns = list(
            filter(
                lambda txt: len(txt) > 1,
                [strip_text(td) for td in table.find_all("td")],
            )
        )

        stats = {}
        for i in range(0, len(columns), 2):
            name = columns[i].lower()
            value = columns[i + 1]

            stats[name] = value

        return stats

    @staticmethod
    def get_weapons(soup: BeautifulSoup) -> [Weapon]:
        weapons = []

        def get_category_weapons(category: str):
            cat_heading = soup.find(id=category)

            if cat_heading is None:
                print(f"Could not find weapon category '{category}'")
                return None

            description = None
            if category != "Unobtainable_Weapons":
                description = strip_text(cat_heading.find_next("p"))

            table = cat_heading.find_next("tbody")
            rows = table.find_all("tr")

            items = []
            for row in rows:
                cols = row.find_all("td")[1:]

                if len(cols) == 0:
                    continue

                fields_lst = [
                    "name",
                    "type",
                    "level",
                    "description",
                    "damage",
                    "critical strike chance",
                    "stats",
                    "location",
                    "purchase price",
                    "sell price",
                ]
                # ordered set hack
                fields = dict.fromkeys(fields_lst)

                # slingshots have neither level nor stats information
                if category == "Slingshot":
                    fields.pop("level")
                    fields.pop("stats")
                if category != "Unobtainable_Weapons":
                    fields.pop("type")
                else:
                    fields.pop("location")
                    fields.pop("purchase price")

                item = {}
                for (i, field) in enumerate(fields.keys()):
                    if field == "stats":
                        item[field] = normalized_stats(cols[i])
                    else:
                        if field == "name":
                            item["reference"] = cols[i].find_next("a").get("href")

                        item[field] = strip_text(cols[i])

                items.append(item)

            return {"description": description, "items": items}

        categories = ["Sword", "Dagger", "Club", "Slingshot", "Unobtainable_Weapons"]

        for category in categories:
            weapons.append(get_category_weapons(category))

        return weapons