from urllib.parse import urljoin

from scrapper.constants import WIKI_URL


def make_wiki_url(uri: str):
    return urljoin(WIKI_URL, uri)
