import logging
from .album_art import init as init_album_art
from .lyrics import init as init_lyrics

logger: logging.Logger


def init():
    global logger
    logger = logging.getLogger(__name__)

    init_album_art()
    init_lyrics()

    logger.info('Base extras plugin loaded')
