from flask import Flask

import server
import database
import settings
import plugin_loader
from plugins.base.television.models import Show, Season, Episode


def test_app_start():
    app: Flask = Flask(__name__)
    server.app = app

    server.__start__()
    settings.__start__()
    database.__start__()

    plugin_loader.__start__()


def test_import():
    with server.app.test_client() as c:
        rv = c.post('/import/tv')
        assert rv.status_code == 201
        res = rv.json
        assert res['message'] == 'Import successful'


def test_show_exists():
    show = database.db.session.query(Show).filter_by(name='The Code Show').one()
    assert show is not None
    assert show.name == 'The Code Show'
    assert show.name_sort == 'Code Show'
    assert type(show.id) == int


def test_season_exists():
    season = database.db.session.query(Season).filter_by(name='Season 01').one()
    assert season is not None
    assert season.name == 'Season 01'
    assert season.number == 1
    assert type(season.id) == int


def test_episode_exist():
    episodes = database.db.session.query(Episode).filter(Episode.season.has(name='Season 01')).all()
    assert episodes is not None
    assert len(episodes) == 10

    episodes = sorted(episodes, key=lambda x: x.number)
    episode = episodes[0]

    assert episode.name == 'aaaaa'
    assert episode.name_sort == 'aaaaa'
    assert type(episode.id) == int
