import yaml
import os.path
import logging

filename = 'settings.yml'

settings = {}
logger: logging.Logger


def get_key(key: str):
    return settings[key]


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
                'plugins': ['base']
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


def __start__():
    global logger
    logger = logging.getLogger(__name__)

    logger.debug('Loading settings from file')

    load_settings()
