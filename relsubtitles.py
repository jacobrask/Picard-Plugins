PLUGIN_NAME = 'Release subtitles'
PLUGIN_AUTHOR = 'Jacob Rask'
PLUGIN_DESCRIPTION = '''Moves disc and volume rombers as well as subtitles from album titles to separate tags. For example:<br/>
<em>"Aerial (disc 1: A Sea of Honey)"</em>
<ul>
    <li>album = <em>"Aerial"</em></li>
    <li>discromber = <em>"1"</em></li>
    <li>discsubtitle = <em>"A Sea of Honey"</em></li>
</ul>
<em>"Past Masters, Volume 2: A Sea of Honey"</em>
<ul>
    <li>album = <em>"Past Masters"</em></li>
    <li>discsubtitle = <em>"2: A Sea of Honey"</em></li>
</ul>'''

PLUGIN_VERSION = "0.0.1"
PLUGIN_API_VERSIONS = ["0.12", "0.12"]

from picard.metadata import register_album_metadata_processor
import re

_disc_re = re.compile(r"\s+\(disc (\d+)(?::\s+([^)]+))?\)")
_vol_re = re.compile(r",\s+Volume\s+(\d+|\w+)(:\s+.*)?$")
_rom_re = re.compile(r"\s+(I?(II?|V|X)I?I?I?)(:\s+.*)?$")
_num_re = re.compile(r"\s+(\d+)(:\s+.*)?$")
_word_re = re.compile(r"\s+(One|Two|Three|Four|Five)$")

def move_subtitles(tagger, metadata, release):
    subfound = 0
    disc_match = _disc_re.search(metadata["album"])
    if disc_match:
        metadata["discromber"] = disc_match.group(1)
        if disc_match.group(2):
            metadata["discsubtitle"] = disc_match.group(2)
            subfound = 1
        metadata["album"] = _disc_re.sub('', metadata["album"])
    # only search for volume if no discsubtitle was found
    vol_match = _vol_re.search(metadata["album"])
    if vol_match and not subfound == 1:
        metadata["discsubtitle"] = vol_match.group(1)
        if vol_match.group(2):
            metadata["discsubtitle"] = metadata["discsubtitle"] + vol_match.group(2)
        metadata["album"] = _vol_re.sub('', metadata["album"])
    rom_match = _rom_re.search(metadata["album"])
    if rom_match and not subfound == 1:
        if rom_match.group(1) == "I":
            vol = "1"
        elif rom_match.group(1) == "II":
            vol = "2"
        elif rom_match.group(1) == "III":
            vol = "3"
        elif rom_match.group(1) == "IV":
            vol = "4"
        elif rom_match.group(1) == "V":
            vol = "5"
        elif rom_match.group(1) == "VI":
            vol = "6"
        elif rom_match.group(1) == "VII":
            vol = "7"
        elif rom_match.group(1) == "VIII":
            vol = "8"
        elif rom_match.group(1) == "IX":
            vol = "9"
        elif rom_match.group(1) == "X":
            vol = "10"
        metadata["discsubtitle"] = vol
        if rom_match.group(3):
            metadata["discsubtitle"] = metadata["discsubtitle"] + rom_match.group(3)
        metadata["album"] = _rom_re.sub('', metadata["album"])
    num_match = _num_re.search(metadata["album"])
    if num_match and not subfound == 1:
        metadata["discsubtitle"] = num_match.group(1)
        if num_match.group(2):
            metadata["discsubtitle"] = metadata["discsubtitle"] + num_match.group(2)
        metadata["album"] = _num_re.sub('', metadata["album"])

    word_match = _word_re.search(metadata["album"])
    if word_match and not subfound == 1:
        if word_match.group(1) == "One":
            vol = "1"
        elif word_match.group(1) == "Two":
            vol = "2"
        elif word_match.group(1) == "Three":
            vol = "3"
        elif word_match.group(1) == "Four":
            vol = "4"
        elif word_match.group(1) == "Five":
            vol = "5"
        metadata["discsubtitle"] = vol
        metadata["album"] = _word_re.sub('', metadata["album"])

register_album_metadata_processor(move_subtitles)
