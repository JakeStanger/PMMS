import logging
import settings
import importlib

logger: logging.Logger


def _load_modules():
    modules = settings.get_key('plugins')
    for module in modules:
        plugin = importlib.import_module('plugins.%s' % module)
        plugin.init()


def __start__():
    global logger
    logger = logging.getLogger(__name__)

    logger.debug('Loading plugins')
    _load_modules()
