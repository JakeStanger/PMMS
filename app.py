from flask import Flask

import server
import settings
import database
import plugin_loader
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app: Flask = Flask(__name__)
server.app = app

settings.__start__()
server.__start__()
database.__start__()

plugin_loader.__start__()

# These should always be the last things to init, in this order
database.__create_all__()


if __name__ == '__main__':
    app.run()
