from flask import Flask
import logging

app: Flask = Flask(__name__)
logger: logging.Logger


@app.route('/')
def hello_world():
    return 'Hello World!'


def __start__():
    logger.debug('Starting Flask server.')
    app.run()


def __init__():
    global app
    global logger

    logger = logging.getLogger(__name__)
    app.app_context().push()
