import re


def strip_text(elm) -> str:
    """Removes trailing spaces from element's text"""
    return elm.text.strip("\n ")


def normalized_stats(stats) -> dict:
    """Get a dictionary from the given item stats"""
    pat = re.compile(r"([A-Za-z .]+)(\xa0| )\(([+-]*\d+%?)\)")
    return dict((stat[0].strip().lower(), stat[2]) for stat in pat.findall(stats))
