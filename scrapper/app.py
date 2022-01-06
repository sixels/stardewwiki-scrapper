import sqlite3
import requests
import json
from os import path, environ, makedirs
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapper.pages.weapons import Weapons
from scrapper.pages.items import Items

CACHE_DIRECTORY = path.join(
    environ.get("XDG_CACHE_HOME", "%s/.cache/" % environ.get("HOME")),
    "stardewcs/")

WIKI_URL = "https://stardewvalleywiki.com/"


def cache_request(url, location):
    if not path.isfile(location):
        res = requests.get(url)
        print(f"GET ${res.status_code} {url}")
        content = res.text

        with open(location, "w") as f:
            f.write(content)

        return content
    else:
        print(f"Cache for {url} already exists at {location}")
        with open(location, "r") as f:
            return f.read()


def save_page(db, page):
    url = urljoin(WIKI_URL, page)
    res = cache_request(url, path.join(CACHE_DIRECTORY, f"{page}.html"))

    soup = BeautifulSoup(res, "html.parser")

    weapons = Weapons.get_weapons(soup)

    for name, category in weapons.items():
        w: dict = dict()
        for w in category["items"]:
            ref = w.pop("reference")
            if ref:
                url = urljoin(WIKI_URL, ref[1:])
                res = cache_request(
                    url, path.join(CACHE_DIRECTORY, f"{ref[1:]}.html"))
                soup = BeautifulSoup(res, "html.parser")
                i = Items.item_info(soup)
                cols = ",".join(i.keys()).replace(" ", "_")
                db.execute(
                    "INSERT INTO ITEMS (name,description,notes,aditional) VALUES (?,?,?,?)",
                    (i["name"], i.get("description"), i.get("notes"),
                     json.dumps(i["aditional"], separators=(",", ":"))))

            if w.get("type") is None:
                w["type"] = name

            if price := w.get("purchase price"):
                if price == "N/A":
                    w["purchase price"] = None
                else:
                    try:
                        w["purchase price"] = int(price[:-1].replace(",", ""))
                    except ValueError:
                        w["purchase price"] = None

            if price := w.get("sell price"):
                if price == "N/A":
                    w["purchase price"] = None
                else:
                    try:
                        w["sell price"] = int(price[:-1].replace(",", ""))
                    except ValueError:
                        w["sell price"] = None

            cols = ",".join(w.keys()).replace("critical strike chance",
                                              "critical_chance").replace(
                                                  " ", "_")
            values = tuple(w.values())

            db.execute(
                f"INSERT INTO weapons ({cols}) VALUES ({', '.join('?'* len(values))});",
                values)


def main():
    makedirs(CACHE_DIRECTORY, exist_ok=True)

    with sqlite3.connect('stardew.db') as conn:
        create_db(conn)
        conn.commit()
