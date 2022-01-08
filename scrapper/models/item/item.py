from typing import TypedDict, List, Union

from bs4 import BeautifulSoup

from scrapper.utils import strip_text


class ItemInfo(TypedDict):
    """A generic item information"""

    """Item name"""
    name: str
    """Item descriptions"""
    descriptions: List[str]
    """Item notes"""
    notes: List[str]
