PLUGIN_NAME = 'Move metadata to version tag'
PLUGIN_AUTHOR = 'Jacob Rask'
PLUGIN_DESCRIPTION = 'Moves song metadata such as "demo", "live" from title and titlesort to version tag.'
PLUGIN_VERSION = "0.1.4"
PLUGIN_API_VERSIONS = ["0.12", "0.15"]

from picard.metadata import register_track_metadata_processor
import re

_p_re = re.compile(r"\(.*?\)")
_v_re = re.compile(r"((\s|-)?(acoustic|akustisk|album|bonus|clean|club|cut|C=64|dance|dirty|disco|encore|extended|inch|maxi|live|original|radio|redux|rehearsal|reprise|reworked|ringtone|[Ss]essions?|short|studio|take|variant|version|vocal)(\s|-)?|.*?(capp?ella)\s?|(\s|-)?(alternat|demo|dub|edit|ext|fail|instr|long|orchestr|record|remaster|remix|strument|[Tt]ape|varv).*?|.*?(complete|mix|inspel).*?)")

def add_title_version(tagger, metadata, release, track):
    if metadata["titlesort"]:
        title = metadata["titlesort"]
    else:
        title = metadata["title"]
    pmatch = _p_re.findall(title)
    if pmatch: # if there's a parenthesis, investigate
        pstr = pmatch[-1][1:-1] # get last match and strip paranthesis
        vmatch = _v_re.search(pstr)
        if vmatch:
            metadata["titlesort"] = re.sub("\(" + pstr + "\)", "", title).strip()
            metadata["title"] = re.sub("\(" + pstr + "\)", "", title).strip()
            metadata["version"] = pstr

register_track_metadata_processor(add_title_version)
