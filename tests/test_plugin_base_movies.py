import server
import database
import settings
import plugin_loader
from plugins.base.movies.models import Movie


def test_app_start():
    server.__start__()
    settings.__start__()
    database.__start__()

    plugin_loader.__start__()


def test_import():
    with server.app.test_client() as c:
        rv = c.post('/import/movies')
        assert rv.status_code == 201
        res = rv.json
        assert res['message'] == 'Import successful'


def test_movie_exists():
    movies = database.db.session.query(Movie).all()
    assert movies is not None
    assert len(movies) == 1

    movie = database.db.session.query(Movie).filter_by(name='The Code Movie').one()
    assert movie is not None
    assert movie.name == 'The Code Movie'
    assert movie.name_sort == 'Code Movie'
    assert movie.release_date.year == 2019
    assert type(movie.id) == int
