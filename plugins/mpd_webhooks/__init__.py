import logging

import settings
from .routes import *

logger: logging.Logger


def init():
    global logger
    logger = logging.getLogger(__name__)

    logger.info('mpd webhooks plugin loaded')

    settings_set = settings.SettingsSet('plugins.mpd_webhooks')

    settings_set.register_key('mpd_host', 'localhost')
    settings_set.register_key('mpd_port', 6600)
