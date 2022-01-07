import re


def strip_text(elm) -> str:
    return elm.text.strip("\n ")


def normalized_stats(stats) -> list[str]:
    pat = re.compile(r"([A-Za-z .]+)(\xa0| )\(([+-]*\d+%?)\)")
    return dict((stat[0].strip().lower(), stat[2]) for stat in pat.findall(stats))
