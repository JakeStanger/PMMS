from flask import Flask

import server
import database
import settings
import plugin_loader
from plugins.base.music.models import Album, Track


def test_app_start():
    app: Flask = Flask(__name__)
    server.app = app

    server.__start__()
    settings.__start__()
    database.__start__()

    settings.set_key('plugins.base_extra', {})

    plugin_loader.__start__()


api_key: str


def test_get_api_key():
    global api_key
    with server.app.test_client() as c:
        rv = c.post('/users/login', data=dict(username='test', password='helloworld'))
        api_key = rv.json['api_key']


def test_local_album_art():
    album = database.db.session.query(Album).filter_by(name='World').one()

    with server.app.test_client() as c:
        rv = c.get('/api/albums/%s/art' % album.id, headers={'Authorization': api_key})
        assert rv.status_code == 200
        assert rv.data is not None
        assert type(rv.data[0]) == int  # Check binary string


def test_lyrics_cache():
    track = database.db.session.query(Track).filter_by(name='Hello World').one()

    with server.app.test_client() as c:
        rv = c.get('/api/tracks/%s/lyrics' % track.id, headers={'Authorization': api_key})
        assert rv.status_code == 200

        lyrics = rv.json
        assert lyrics is not None
        assert 'lyrics' in lyrics
        assert 'Hello World' in lyrics['lyrics']
