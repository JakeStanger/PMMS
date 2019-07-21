import settings
import os

settings.__start__()


def test_settings_file_exists():
    assert os.path.isfile('settings.yml')


def test_settings_exist():
    assert settings.settings is not None
    assert type(settings.settings) == dict


def test_set_key():
    settings.set_key('test.key', 'Hello World')
    assert settings.get_key('test.key') == 'Hello World'


def test_register_key():
    settings.register_key('test.default', 'Hello World')
    assert settings.get_key('test.default') == 'Hello World'


def test_database_key():
    database = settings.get_key('database')
    assert database is not None
    assert type(database) == str


def test_plugins_key():
    plugins = settings.get_key('plugins')
    assert plugins is not None
    assert type(plugins) == dict


def test_secret_key():
    secret = settings.get_key('secret_key')
    assert secret is not None
    assert type(secret) == str
