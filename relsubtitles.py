PLUGIN_NAME = 'Release subtitles'
PLUGIN_AUTHOR = 'Jacob Rask'
PLUGIN_DESCRIPTION = '''Moves disc and volume numbers as well as subtitles from album titles to separate tags. For example:<br/>
<em>"Aerial (disc 1: A Sea of Honey)"</em>
<ul>
    <li>album = <em>"Aerial"</em></li>
    <li>discnumber = <em>"1"</em></li>
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
_vol_re = re.compile(r",\s+Volume\s+(\d+|\w+|[IVX])(:\s+.*)?")

def move_subtitles(tagger, metadata, release):
    disc_match = _disc_re.search(metadata["album"])
    vol_match = _vol_re.search(metadata["album"])
    subfound = 0
    if disc_match:
        metadata["discnumber"] = disc_match.group(1)
        if disc_match.group(2):
            metadata["discsubtitle"] = disc_match.group(2)
            metadata["album"] = _disc_re.sub('', metadata["album"])
            subfound = 1
    # only search for volume if no discsubtitle was found
    if vol_match and not subfound == 1:
        metadata["discsubtitle"] = vol_match.group(1)
        if vol_match.group(2):
            metadata["discsubtitle"] = metadata["discsubtitle"] + vol_match.group(2)
        metadata["album"] = _vol_re.sub('', metadata["album"])

register_album_metadata_processor(move_subtitles)
