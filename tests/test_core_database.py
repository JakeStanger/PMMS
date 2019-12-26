from flask import Flask

import server
import database
import settings
import plugin_loader

app = Flask(__name__)
app.app_context().push()
server.app = app

settings.__start__()
database.__start__()
plugin_loader.__start__()


def test_database_exists():
    assert database.db is not None


class TestModel(database.db.Model):
    id = database.db.Column(database.db.Integer, primary_key=True)
    name = database.db.Column(database.db.String)


def test_add_column():
    first_name = database.db.Column(database.db.Integer, name='first_name')
    assert first_name is not None
    plugin_loader.add_column(TestModel, first_name)
    assert len(database._column_queue) == 1


def test_create_endpoints():
    plugin_loader.add_api_endpoints(TestModel, ['GET'])


def test_create_all():
    database.__create_all__()


def test_add_row():
    row = TestModel(name='Hello world', first_name='Hello')
    assert row.name == 'Hello world'
    assert row.first_name == 'Hello'
    assert row.id is None

    database.db.session.add(row)
    database.db.session.commit()


def test_get_row():
    row = database.db.session.query(TestModel).filter_by(name='Hello world').one()
    assert row is not None
    assert type(row) == TestModel

    assert row.name == 'Hello world'
    assert row.first_name == 'Hello'
    assert type(row.id) == int


def test_get_row_endpoint():
    with server.app.test_client() as c:
        rv = c.get('/api/test_model/1')

        res = rv.json
        assert res is not None
        assert type(res) == dict
        assert 'data' in res
        assert 'attributes' in res['data']

        attributes = res['data']['attributes']

        assert attributes['name'] == 'Hello world'
        assert attributes['first_name'] == 'Hello'
