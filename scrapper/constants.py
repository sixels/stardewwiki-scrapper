from os import path, environ

CACHE_DIRECTORY = path.join(
    environ.get("XDG_CACHE_HOME", "%s/.cache/" % environ.get("HOME")), "stardew_wiki/"
)

WIKI_URL = "https://stardewvalleywiki.com"
