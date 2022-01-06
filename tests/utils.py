from bs4 import BeautifulSoup

def make_soup(filename: str):
    with open(f"tests/data/{filename}", "r") as f:
        return BeautifulSoup(f.read(), "html.parser")
