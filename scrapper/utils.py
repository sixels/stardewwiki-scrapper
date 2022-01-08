from os import path, makedirs
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests

from scrapper.constants import WIKI_URL, CACHE_DIRECTORY


def strip_text(elm) -> str:
    """Removes trailing spaces from element's text"""
    return elm.text.strip("\n ")


def normalized_stats(stats) -> dict:
    """Get a dictionary from the given item stats"""
    import re

    pat = re.compile(r"([A-Za-z .]+)(\xa0| )\(([+-]*\d+%?)\)")
    return dict((stat[0].strip().lower(), stat[2]) for stat in pat.findall(stats))


def make_soup(page: str) -> BeautifulSoup:
    return BeautifulSoup(page, "html.parser")


def req_cached(url: str) -> str:
    """Send a GET request to the given url and return the response body"""
    cache = path.join(CACHE_DIRECTORY, urlparse(url).path[1:])

    if not path.isfile(cache):
        res = requests.get(url)
        print(f"Saving {url} into {cache}")
        content = res.text

        with open(cache, "w") as f:
            f.write(content)

        return content
    else:
        print(f"Cache for {url} already exists at {cache}")
        with open(cache, "r") as f:
            return f.read()


def make_cache_dir():
    makedirs(CACHE_DIRECTORY, exist_ok=True)
