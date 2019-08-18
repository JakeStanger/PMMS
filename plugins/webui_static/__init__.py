import logging
import settings
from .routes import *

base_settings = settings.SettingsSet('plugins.base')

if base_settings.get_key('music.enable'):
    from .music import *

if base_settings.get_key('movies.enable'):
    from .movies import *

logger: logging.Logger


def init():
    global logger
    logger = logging.getLogger(__name__)

    logger.info('Static web interface loaded')
