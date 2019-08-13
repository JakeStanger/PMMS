from .users import *
from .music import init as init_music
from .movies import init as init_movies
from .television import init as init_television
import logging

logger: logging.Logger


def init():
    global logger
    logger = logging.getLogger(__name__)

    init_music()
    init_movies()
    init_television()

    logger.info('Base plugin loaded')
