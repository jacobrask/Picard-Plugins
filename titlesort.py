PLUGIN_NAME = 'Title sort names'
PLUGIN_AUTHOR = 'Jacob Rask'
PLUGIN_DESCRIPTION = 'Guesses title album sortnames and adds as titlesort and albumsort tags.'
PLUGIN_VERSION = "0.1.3"
PLUGIN_API_VERSIONS = ["0.12", "0.12"]

from picard.metadata import register_track_metadata_processor
from picard.metadata import register_album_metadata_processor
import re

re_articles = {}
re_articles["eng"] = re.compile(r"The |Tha |Da ")
re_articles["esp"] = re.compile(r"El |La |Los |Las ")
re_articles["deu"] = re.compile(r"Der |Das |Die ")
re_articles["fra"] = re.compile(r"Les |Le |La |L'")
re_articles["swe"] = re.compile(r"De |Den |Dom ")
re_articles["mul"] = re.compile(r"The |Tha |Da |El |La |Los |Las |L'|Der |Das |Die |Le |Les |De |Den |Dom ")

def add_titlesort(tagger, metadata, release, track):
    if metadata["titlesort"]:
        titlesort = metadata["titlesort"]
    else:
        titlesort = metadata["title"]
    lang = "mul" # default
    if metadata["language"] and metadata["language"] in re_articles:
        lang = metadata["language"]
    sort_re = re_articles[lang]
    match = sort_re.match(titlesort)
    if match:
        sort_prefix = match.group().strip()
        titlesort = sort_re.sub("", titlesort).strip() + ", " + sort_prefix
        titlesort = titlesort[0].upper() + titlesort[1:] # make sure first letter is capitalized
    metadata["titlesort"] = titlesort

def add_albumsort(tagger, metadata, release):
    if metadata["albumsort"]:
        titlesort = metadata["albumsort"]
    else:
        titlesort = metadata["album"]
    lang = "mul" # default
    if metadata["language"] and metadata["language"] in re_articles:
        lang = metadata["language"]
    sort_re = re_articles[lang]
    match = sort_re.match(titlesort)
    if match:
        sort_prefix = match.group().strip()
        titlesort = sort_re.sub("", titlesort).strip() + ", " + sort_prefix
        titlesort = titlesort[0].upper() + titlesort[1:] # make sure first letter is capitalized
    metadata["albumsort"] = titlesort

register_track_metadata_processor(add_titlesort)
register_album_metadata_processor(add_albumsort)
