import logging

logger: logging.Logger


def init():
    global logger
    logger = logging.getLogger(__name__)

    logger.info('Base module loaded!')
