from .routes import *
from .tables import *
from .scanners.music import *
from .scanners.movies import *
import logging

logger: logging.Logger


def init():
    global logger
    logger = logging.getLogger(__name__)

    logger.info('Base module loaded!')
