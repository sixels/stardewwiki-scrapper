def strip_text(elm) -> str:
    return elm.text.strip("\n ")

def normalized_stats(stats):
    return strip_text(stats)              \
        .replace('\xa0', ' ')             \
        .replace("Vampiric", " Vampiric")
