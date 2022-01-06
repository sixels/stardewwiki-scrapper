from bs4 import BeautifulSoup

from scrapper.utils import strip_text,normalized_stats

class Items():
    @staticmethod
    def item_info(soup: BeautifulSoup) -> dict:
        heading = soup.find(id="firstHeading")


        if heading is None:
            print("Could not find weapon info")
            return {}

        desc_p = soup.find(id="infoboxborder")
        if not desc_p:
            return {}

        desc_p = desc_p.find_next_siblings()

        descriptions = []
        for p in desc_p:
            if p:
                if p.name != "p" and len(descriptions) > 0:
                    break
                if p.name == "p": descriptions.append(p)

        name = strip_text(heading)
        description = '\n'.join([strip_text(p) for p in
            descriptions])

        notes = soup.find(id="Notes")
        if notes is not None:
            notes = strip_text(notes.find_next("ul"))

        infos = { "name": name, "description": description, "notes": notes }

        info_box = soup.find(id="infoboxtable")
        if info_box is None:
            print("Could not find the info box")
            return infos
        aditional = {}

        rows = info_box.find_all("tr")[2:]

        details = strip_text(rows[0].find_next(id="infoboxdetail"))

        section = None
        for row in rows[1:]:
            col = row.find_next("td");

            if col['id'] == "infoboxsection":
                col_val = col.find_next_sibling();
                if col_val is None:
                    section = strip_text(col)
                    aditional[section] = {}
                else:
                    # the last character is a colon
                    key = strip_text(col)[:-1]

                    value = strip_text(col_val) if key != "Stats" else \
                            normalized_stats(col_val)

                    if section is not None:
                        aditional[section][key] = value
                    else:
                        aditional[key] = value

        aditional["details"] = details
        infos["aditional"] = aditional
        return infos


