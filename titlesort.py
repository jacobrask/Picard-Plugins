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
articles['deu'] = ['Der ', 'Das ', 'Die ', 'Eine? '] # German
articles['eng'] = ['Th(e|a) ', 'Da ', 'An? '] # English
articles['esp'] = ['El ', 'La ', 'L(o|a)s ', 'Una? ', 'Un(o|a)s '] # Spanish
articles['fra'] = ['L(e|a)s? ', 'L\'', 'Une? ', 'Des '] # French
articles['ita'] = ['Il ', 'L(o|a|e) ', 'L\'', 'I ', 'Gli ', 'Un(o|a)? ', 'Un\''] # Italian
articles['swe'] = ['Den? ', 'Dom '] # Swedish

# compile sort language regular expressions
re_articles = {}
regmul = ''
for lang, a in articles.iteritems():
    reg = ''
    for i in range(len(a)):
        reg = '|' + articles[lang][i] + reg
        re_articles[lang] = re.compile(reg)
    regmul = regmul + reg
# all articles are collected and used for "multiple languages"
re_articles['mul'] = re.compile(regmul[1:])

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
