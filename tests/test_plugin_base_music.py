from flask import Flask

import server
import database
import settings
import plugin_loader
from plugins.base.music.models import Artist, Album, Track


def test_app_start():
    app: Flask = Flask(__name__)
    server.app = app

    server.__start__()
    settings.__start__()
    database.__start__()

    plugin_loader.__start__()


def test_import():
    with server.app.test_client() as c:
        rv = c.post('/import/music')
        assert rv.status_code == 201
        res = rv.json
        assert res['message'] == 'Import successful'


def test_artist_exists():
    artist = database.db.session.query(Artist).filter_by(name='Hello').one()
    assert artist is not None
    assert artist.name == 'Hello'
    assert artist.name_sort == 'Hello'
    assert type(artist.id) == int


def test_album_exists():
    album = database.db.session.query(Album).filter_by(name='World').one()
    assert album is not None
    assert album.name == 'World'
    assert album.name_sort == 'World'
    assert type(album.id) == int


def test_tracks_exist():
    tracks = database.db.session.query(Track).filter(Track.album.has(name='World')).all()
    assert tracks is not None
    assert len(tracks) == 10

    tracks = sorted(tracks, key=lambda x: x.track_num)
    track = tracks[0]

    assert track.name == 'Hello World'
    assert track.name_sort == 'Hello World'
    assert type(track.id) == int
