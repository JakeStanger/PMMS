import server
import database
import settings
import plugin_loader
from plugins.base.users.models import User


def test_app_start():
    server.__start__()
    settings.__start__()
    database.__start__()

    plugin_loader.__start__()


def test_endpoints_require_auth():
    with server.app.test_client() as c:
        rv = c.get('/api/artists')
        assert rv.status_code == 401


def test_create_user():
    with server.app.test_client() as c:
        rv = c.post('/users/signup', data=dict(username='test', password='helloworld'))
        assert rv.status_code == 201
        res = rv.json
        assert res['message'] == 'User created'


def test_user_exists():
    user = database.db.session.query(User).filter_by(username='test').one()
    assert user is not None
    assert user.username == 'test'

    assert user.password != 'helloworld'  # Check it's been encrypted
    assert user.password is not None

    assert not user.is_admin
    assert not user.is_deleted
    assert len(user.api_key) == 64
    assert type(user.id) == int


def test_login_invalid_username():
    with server.app.test_client() as c:
        rv = c.post('/users/login', data=dict(username='invalid', password='zzzzing'))
        assert rv.status_code == 401

        res = rv.json
        assert res['message'] == 'Invalid username'


def test_login_invalid_password():
    with server.app.test_client() as c:
        rv = c.post('/users/login', data=dict(username='test', password='zzzzing'))
        assert rv.status_code == 401

        res = rv.json
        assert res['message'] == 'Invalid password'


def test_login_valid():
    with server.app.test_client() as c:
        rv = c.post('/users/login', data=dict(username='test', password='helloworld'))
        assert rv.status_code == 202

        res = rv.json
        assert res['username'] == 'test'
        assert len(res['api_key']) == 64


def test_access_endpoint_with_auth():
    user = database.db.session.query(User).filter_by(username='test').one()
    with server.app.test_client() as c:
        rv = c.get('/api/artists', headers={'Authorization': user.api_key})
        assert rv.status_code == 200
