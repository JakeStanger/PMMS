import server
import database
import settings
import plugin_loader
from plugins.base.music.models import Album, Track
import mimetypes


def test_app_start():
    server.__start__()
    settings.__start__()
    database.__start__()

    plugin_loader.__start__()


def test_local_album_art():
    album = database.db.session.query(Album).filter_by(name='World').one()

    with server.app.test_client() as c:
        rv = c.get('/api/albums/%s/art' % album.id)
        assert rv.status_code == 200
        assert rv.content is not None
        assert mimetypes.guess_type(rv.content) == 'image/jpeg'


def test_lyrics_cache():
    track = database.db.session.query(Track).filter_by(name='Hello World').one()

    with server.app.test_client() as c:
        rv = c.get('/api/tracks/%s/lyrics' % track.id)
        assert rv.status_code == 200

        lyrics = rv.json
        assert lyrics is not None
        assert 'lyrics' in lyrics
        assert 'Hello World' in lyrics['lyrics']
