import sqlite3
import requests
import json
from os import path, environ, makedirs
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapper.db import create_db

from scrapper.pages.url import make_wiki_url
from scrapper.pages import Weapons, Villagers
from scrapper.models.item import Weapon
from scrapper.models.villager import Villager

from scrapper.utils import req_cached, make_soup
from scrapper.constants import WIKI_URL, CACHE_DIRECTORY


def main():
    makedirs(CACHE_DIRECTORY, exist_ok=True)

    with sqlite3.connect("stardew.db") as conn:
        cursor = create_db(conn)

        for uri in Weapons.get_pages(Weapons.request_wiki()):
            weapon_soup = make_soup(req_cached(make_wiki_url(uri)))
            weapon = Weapon.parse(weapon_soup)

        for uri in Villagers.get_pages(Villagers.request_wiki()):
            villager_soup = make_soup(req_cached(make_wiki_url(uri)))
            villager = Villager.parse(villager_soup)

        conn.commit()


# def save_page(db, page):
#     wiki_url = urljoin(WIKI_URL, page)
#     res = req_cached(wiki_url, path.join(CACHE_DIRECTORY, f"{page}.html"))
#     soup = BeautifulSoup(res, "html.parser")

#     weapons = Weapons.get_weapons()

#     for name, category in weapons.items():
#         w: dict = dict()
#         for w in category["items"]:
#             ref = w.pop("reference")
#             if ref:
#                 url = urljoin(WIKI_URL, ref[1:])
#                 res = req_cached(
#                     wiki_url, path.join(CACHE_DIRECTORY, "%s.html" % ref[1:])
#                 )
#                 soup = BeautifulSoup(res, "html.parser")
#                 i = Items.item_info(soup)
#                 cols = ",".join(i.keys()).replace(" ", "_")
#                 db.execute(
#                     "INSERT INTO ITEMS (name,description,notes,aditional) VALUES (?,?,?,?)",
#                     (
#                         i["name"],
#                         i.get("description"),
#                         i.get("notes"),
#                         json.dumps(i["aditional"], separators=(",", ":")),
#                     ),
#                 )

#             if w.get("type") is None:
#                 w["type"] = name

#             if price := w.get("purchase price"):
#                 if price == "N/A":
#                     w["purchase price"] = None
#                 else:
#                     try:
#                         w["purchase price"] = int(price[:-1].replace(",", ""))
#                     except ValueError:
#                         w["purchase price"] = None

#             if price := w.get("sell price"):
#                 if price == "N/A":
#                     w["purchase price"] = None
#                 else:
#                     try:
#                         w["sell price"] = int(price[:-1].replace(",", ""))
#                     except ValueError:
#                         w["sell price"] = None

#             cols = (
#                 ",".join(w.keys())
#                 .replace("critical strike chance", "critical_chance")
#                 .replace(" ", "_")
#             )
#             values = tuple(w.values())

#             db.execute(
#                 f"INSERT INTO weapons ({cols}) VALUES ({', '.join('?'* len(values))});",
#                 values,
#             )
