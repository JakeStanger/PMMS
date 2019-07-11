from flask import Flask
import logging
import settings

app: Flask = Flask(__name__)
logger: logging.Logger


@app.route('/')
def hello_world():
    return 'Hello World!'


def __run__():
    logger.debug('Starting Flask server.')

    app.secret_key = settings.get_key('secret_key')

    app.run()


def __start__():
    global app
    global logger

    logger = logging.getLogger(__name__)
    app.app_context().push()
