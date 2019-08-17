import yaml
import os.path
import logging
import helpers

filename = 'settings.yml'

settings = {}
logger: logging.Logger


class SettingsSet:
    base_path: str

    def __init__(self, base_path: str):
        self.base_path = base_path

    def get_full_path(self, path: str):
        return '%s.%s' % (self.base_path, path)

    def get_key(self, path: str):
        return get_key(self.get_full_path(path))

    def set_key(self, path: str, value):
        set_key(self.get_full_path(path), value)

    def register_key(self, path, default):
        register_key(self.get_full_path(path), default)


def register_key(path: str, default):
    logger.debug('Registering default value for \'%s\'' % path)
    if get_key(path) is None:
        set_key(path, default)


def get_key(path: str):
    global settings

    keys = path.split('.')

    rv = settings
    for path in keys:
        if rv and path in rv:
            rv = rv[path]
        else:
            return None
    return rv


def set_key(path: str, value):
    global settings

    logger.debug('Setting \'%s\' to \'%s\'' % (path, value))

    keys = path.split('.')

    rv = settings

    for i, path in enumerate(keys):
        if path not in rv or rv[path] is None:
            rv[path] = {}

        if i == len(keys)-1:
            rv[path] = value
        else:
            rv = rv[path]


def check_and_create_file():
    """
    Makes sure the settings file exists.
    If it doesn't a new one is created with defaults.
    """
    if not os.path.isfile('settings.yml'):
        logger.warning('Settings file was not found. A new one was created.')
        with open(filename, 'w') as f:
            base_settings = {
                'database': 'sqlite:///database.db',
                'plugins': {'base': {}},
                'secret_key': helpers.generate_secret_key()
            }

            f.write(yaml.dump(base_settings, default_flow_style=False))


def load_settings():
    """
    Loads settings from YAML into a global dict.
    """
    global settings

    check_and_create_file()
    with open(filename, 'r') as f:
        settings = yaml.load(f.read(), Loader=yaml.FullLoader)


def save_settings():
    """
    Saves settings from global dict into YAML file
    """
    global settings

    with open(filename, 'w') as f:
        f.write(yaml.dump(settings, default_flow_style=False))


def __start__():
    global logger
    logger = logging.getLogger(__name__)

    logger.debug('Loading settings from file')

    load_settings()
