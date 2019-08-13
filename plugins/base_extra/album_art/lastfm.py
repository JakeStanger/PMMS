import io
from urllib.request import urlopen

import settings
import pylast as pl
from plugins.base.music.models import Album


def fetch_lastfm_art(album: Album):
    api_key = settings.get_key('plugins.base_extra.music.album_art.lastfm.api_key')

    network = pl.LastFMNetwork(api_key=api_key)
    url = network.get_album(album.artist.name, album.name).get_cover_image()
    return io.BytesIO(urlopen(url).read()) if url else None
