from os import path, makedirs
from urllib.parse import urlparse
from typing import List

from bs4 import BeautifulSoup
import requests

from scrapper.constants import WIKI_URL, CACHE_DIRECTORY


def strip_text(elm) -> str:
    """Removes trailing spaces from element's text"""
    return elm.text.strip("\n \xa0") if elm else ""


def normalized_stats(stats) -> dict:
    """Get a dictionary from the given item stats"""
    import re

    pat = re.compile(r"([A-Za-z .]+)(\xa0| )\(([+-]*\d+%?)\)")
    return dict((stat[0].strip().lower(), stat[2]) for stat in pat.findall(stats))


def normalized_list(string: str) -> List[str]:
    """Get a list from the given string"""
    import re

    pat = re.compile(r"([A-Za-z \.]+)(\xa0| )\(([+-]?\w*%?)\)")
    lst = [
        groups[0].strip().capitalize() + " (" + groups[2] + ")"
        for groups in pat.findall(string)
    ]
    return lst if len(lst) else [string]


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
        # print(f"Cache for {url} already exists at {cache}")
        with open(cache, "r") as f:
            return f.read()


def make_cache_dir():
    makedirs(CACHE_DIRECTORY, exist_ok=True)
