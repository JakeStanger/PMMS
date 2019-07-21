import server
import database
import settings
import plugin_loader

settings.__start__()
server.__start__()
database.__start__()
plugin_loader.__start__()


def test_database_exists():
    assert database.db is not None


class TestModel(database.db.Model):
    id = database.db.Column(database.db.Integer, primary_key=True)
    name = database.db.Column(database.db.String)


# TODO: Fix test (probably after some refactoring)
def test_add_column():
    first_name = database.db.Column(database.db.Integer, name='first_name')
    assert first_name is not None
    plugin_loader.add_column('test_model', first_name)
    assert len(database._column_queue) == 1


database.__create_all__()


def test_add_row():
    row = TestModel(name='Hello world'
                    # , first_name='Hello'
                    )
    assert row.name == 'Hello world'
    # assert row.first_name == 'Hello'
    assert row.id is None

    database.db.session.add(row)
    database.db.session.commit()


def test_get_row():
    row = database.db.session.query(TestModel).filter_by(name='Hello world').one()
    assert row is not None
    assert type(row) == TestModel

    assert row.name == 'Hello world'
    # assert row.first_name == 'Hello'
    assert type(row.id) == int
