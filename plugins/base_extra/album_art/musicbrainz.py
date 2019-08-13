import io
import musicbrainzngs as mb
from plugins.base.music.models import Album


def fetch_musicbrainz_art(album: Album):
    releases = mb.search_releases(artist=album.artist.name, release=album.name, limit=10)['release-list']

    cover = None
    i = 0
    while not cover and i < len(releases):
        try:
            cover = mb.get_image_front(releases[i]['id'])
        except mb.ResponseError:
            i += 1
    if cover:
        return io.BytesIO(cover)
