import logging
import server

logger: logging.Logger


@server.app.route('/base')
def base():
    return "Base endpoint! Loaded from %s " % __name__
