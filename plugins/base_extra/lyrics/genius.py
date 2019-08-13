import lyricsgenius
import settings
from plugins.base.music import Track


def fetch_genius_lyrics(track: Track):
    api_key = settings.get_key('plugins.base_extra.music.lyrics.genius.api_key')
    genius = lyricsgenius.Genius(api_key)

    try:
        return genius.search_song(track.name, track.artist.name).lyrics
    except ConnectionError:
        return None
