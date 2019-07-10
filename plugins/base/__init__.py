from .routes import *
from .tables import *
import logging


def init():
    global logger
    logger = logging.getLogger(__name__)

    logger.info('Base module loaded!')
