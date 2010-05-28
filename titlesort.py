PLUGIN_NAME = 'Title sort names'
PLUGIN_AUTHOR = 'Jacob Rask'
PLUGIN_DESCRIPTION = 'Guesses title and album sortnames (language specific) and adds as titlesort and albumsort tags.'
PLUGIN_VERSION = "0.1.3"
PLUGIN_API_VERSIONS = ["0.12", "0.12"]

from picard.metadata import register_track_metadata_processor
from picard.metadata import register_album_metadata_processor
import re

# define articles
articles = {}
articles['eng'] = ['The', 'Tha', 'Da']
articles['esp'] = ['El', 'La', 'Los', 'Las']
articles['deu'] = ['Der', 'Das', 'Die']
articles['fra'] = ['Les', 'Le', 'La']
articles['swe'] = ['De', 'Den', 'Dom']

# compile regular expressions
re_articles = {}
for lang in articles:
    for n in range(len(articles[lang])):
        if n == 0:
            reg = articles[lang][n]
        else:
            reg = reg + ' |' + articles[lang][n]
        re_articles[lang] = re.compile(reg)

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
        titlesort = titlesort[0].upper() + titlesort[1:] # capitalize first letter
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
        titlesort = titlesort[0].upper() + titlesort[1:] # capitalize first letter
    metadata["albumsort"] = titlesort

register_track_metadata_processor(add_titlesort)
register_album_metadata_processor(add_albumsort)
