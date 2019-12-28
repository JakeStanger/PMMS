import lyricsgenius
import settings
from plugins.base.music import Track


def fetch_genius_lyrics(track: Track):
    api_key = settings.get_key('plugins.base_extra.music.lyrics.genius.api_key')
    genius = lyricsgenius.Genius(api_key)

    try:
        song = genius.search_song(track.name, track.artist.name)
        if song:
            return song.lyrics
        return None

    except ConnectionError:
        return None
