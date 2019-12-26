from flask import Flask
import logging
import settings

app: Flask
logger: logging.Logger


def __start__():
    global app
    global logger

    logger = logging.getLogger(__name__)
    app.secret_key = settings.get_key('secret_key')
    app.app_context().push()
