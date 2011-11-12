PLUGIN_NAME = 'Title sort names'
PLUGIN_AUTHOR = 'Jacob Rask'
PLUGIN_DESCRIPTION = 'Guesses title and album sortnames (language specific) and adds as titlesort and albumsort tags.'
PLUGIN_VERSION = "0.1.4"
PLUGIN_API_VERSIONS = ["0.12", "0.15"]

from picard.metadata import register_track_metadata_processor
from picard.metadata import register_album_metadata_processor
import re

# define articles
_articles = {}
_articles['deu'] = ['Der ', 'Das ', 'Die ', 'Eine? '] # German
_articles['eng'] = ['Th[ae] ', 'Da ', 'An? '] # English
_articles['esp'] = ['El ', 'La ', 'L[ao]s ', 'Una? ', 'Un[ao]s '] # Spanish
_articles['fra'] = ["Les? ", "La ", "L'", "Une? ", "Des "] # French
_articles['ita'] = ["Il ", "L[aeo] ", "L'", "I ", "Gli ", "Un[ao]? ", "Un'"] # Italian
_articles['swe'] = ['De[nt]? ', 'Dom ', 'E(n|tt) '] # Swedish

# compile sort language regular expressions
_re_articles = {}
_regmul = ''
for lang, a in _articles.iteritems():
    reg = ''
    for i in range(len(a)):
        reg = '|^' + _articles[lang][i] + reg
        _re_articles[lang] = re.compile(reg[1:])
    _regmul = _regmul + reg
# all articles are collected and used for "multiple languages"
_re_articles['mul'] = re.compile(_regmul[1:])

def make_sorttitle(title, lang):
    if lang not in _re_articles:
        lang = "mul"
    sort_re = _re_articles[lang]
    match = sort_re.match(title)
    titlesort = title
    if match:
        sort_prefix = match.group().strip()
        titlesort = sort_re.sub("", title).strip() + ", " + sort_prefix
        titlesort = titlesort[0].upper() + titlesort[1:] # capitalize first letter
    return titlesort

def add_titlesort(tagger, metadata, release, track):
    if metadata["titlesort"]:
        titlesort = metadata["titlesort"]
    else:
        titlesort = metadata["title"]
    metadata["titlesort"] = make_sorttitle(titlesort, metadata["language"])

def add_albumsort(tagger, metadata, release):
    if metadata["albumsort"]:
        titlesort = metadata["albumsort"]
    else:
        titlesort = metadata["album"]
    metadata["albumsort"] = make_sorttitle(titlesort, metadata["language"])

register_track_metadata_processor(add_titlesort)
register_album_metadata_processor(add_albumsort)
