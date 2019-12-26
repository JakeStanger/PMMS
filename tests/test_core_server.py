from flask import Blueprint, Flask

import server
import settings
import plugin_loader

app = Flask(__name__)
app.app_context().push()
server.app = app

settings.__start__()
plugin_loader.__start__()


def test_create_endpoint():
    @server.app.route('/test')
    def test_endpoint():
        return "Hello world"

    with server.app.test_client() as c:
        rv = c.get('/test')
        assert rv.data == b'Hello world'


def test_create_blueprint():
    blueprint = plugin_loader.create_blueprint('test_bp', '/testbp', 'tests')
    assert blueprint is not None
    assert type(blueprint) == Blueprint

    assert blueprint.name == 'test_bp'
    assert blueprint.url_prefix == '/testbp'


def test_get_blueprint():
    blueprint = plugin_loader.get_blueprint('test_bp', 'tests')
    assert blueprint is not None
    assert type(blueprint) == Blueprint

    assert blueprint.name == 'test_bp'
    assert blueprint.url_prefix == '/testbp'
