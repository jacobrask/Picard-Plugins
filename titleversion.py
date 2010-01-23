PLUGIN_NAME = 'Move metadata to version tag'
PLUGIN_AUTHOR = 'Jacob Rask'
PLUGIN_DESCRIPTION = 'Moves song metadata from titles to version tags.'
PLUGIN_VERSION = "0.1.1"
PLUGIN_API_VERSIONS = ["0.12", "0.12"]

from picard.metadata import register_track_metadata_processor
import re

p_re = re.compile(r"\(.*?\)")
v_re = re.compile(r"(\s?(acoustic|akustisk|album|bonus|clean|club|cut|C=64|dance|dirty|disco|encore|failure|inch|live|original|radio|redux|rehearsal|reprise|ringtone|session|short|studio|take|variant|version|vocal)\s?|.*?(capella)\s?|\s?(alternat|demo|dub|edit|ext|instr|long).*?|.*?mix.*?)")

def add_title_version(tagger, metadata, release, track):
    title = metadata["title"]
    pmatch = p_re.findall(title)
    if pmatch: # if there's a parenthesis, investigate
        pstr = pmatch[-1][1:-1] # get last match and strip paranthesis
        vmatch = v_re.search(pstr)
        if vmatch:
            metadata["title"] = re.sub("\(" + pstr + "\)", "", title).strip()
            metadata["version"] = pstr

register_track_metadata_processor(add_title_version)