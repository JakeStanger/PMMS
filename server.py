from flask import Flask
import logging
import settings

app: Flask = Flask(__name__)
logger: logging.Logger


def __run__():
    logger.debug('Starting Flask server.')

    app.run(host='0.0.0.0')


def __start__():
    global app
    global logger

    logger = logging.getLogger(__name__)
    app.secret_key = settings.get_key('secret_key')
    app.app_context().push()
