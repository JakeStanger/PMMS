import server
import settings
import database
import os
import os.path
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_directories():
    directories = ['/etc/pmms']
    for directory in directories:
        if not os.path.isdir(directory):
            os.mkdir(directory)


if __name__ == '__main__':
    # create_directories()

    logger.info('Starting services')

    server.__init__()
    settings.__init__()
    database.__init__()

    # These should always be the last things to init, in this order
    database.__create_all__()
    server.__start__()
