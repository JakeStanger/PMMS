from .routes import *
from .tables import *
# from .schema import *
from .scanners.music import *
import logging

logger: logging.Logger


def init():
    global logger
    logger = logging.getLogger(__name__)

    logger.info('Base module loaded!')
