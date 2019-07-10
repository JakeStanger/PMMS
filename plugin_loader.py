import logging
import settings
import server
import importlib
import sys
from flask import Blueprint

logger: logging.Logger


def create_blueprint(bp_name: str, url_prefix: str, module_name: str, ):
    """
    Creates a Flask blueprint which will automatically be registered
    :param bp_name: The blueprint name
    :param url_prefix: The URL prefix for the blueprint
    :param module_name: The module name of the **entry point** for the plugin. e.g `plugins.base`
    :return: The blueprint
    """

    logger.debug('Creating blueprint \'%s\' with prefix \'%s\'' % (bp_name, url_prefix))
    bp = Blueprint(bp_name, __name__, url_prefix=url_prefix)

    if hasattr(sys.modules[module_name], '__blueprints__'):
        existing_bps = getattr(sys.modules[module_name], '__blueprints__')
    else:
        existing_bps = []

    existing_bps.append(bp)
    setattr(sys.modules[module_name], '__blueprints__', existing_bps)

    return bp


def register_bp(bp: Blueprint):
    server.app.register_blueprint(bp)


def _load_modules():
    modules = settings.get_key('plugins')
    for module in modules:
        plugin = importlib.import_module('plugins.%s' % module)

        # Every plugin should have an init entry point
        plugin.init()

        if hasattr(sys.modules[plugin.__name__], '__blueprints__'):
            for bp in plugin.__blueprints__:
                server.app.register_blueprint(bp)


def __start__():
    global logger
    logger = logging.getLogger(__name__)

    logger.debug('Loading plugins')
    _load_modules()
