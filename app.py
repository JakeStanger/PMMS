import server
import settings
import database
import plugin_loader
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info('Starting services')

    settings.__start__()
    server.__start__()
    database.__start__()

    plugin_loader.__start__()

    # These should always be the last things to init, in this order
    database.__create_all__()
    server.__run__()
