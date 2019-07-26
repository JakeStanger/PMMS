import logging
from typing import List

import settings
import server
import importlib
import database
import sys
from flask import Blueprint

logger: logging.Logger


def create_blueprint(bp_name: str, url_prefix: str, module_name: str, ) -> Blueprint:
    """
    Creates a Flask blueprint which will automatically be registered.

    :param bp_name: The blueprint name
    :param url_prefix: The URL prefix for the blueprint
    :param module_name: The module name of the **entry point** for the plugin. e.g `plugins.base`
    :return: The new blueprint
    """

    logger.debug('Creating blueprint \'%s\' with prefix \'%s\'' % (bp_name, url_prefix))

    bp = Blueprint(bp_name, __name__, url_prefix=url_prefix)

    if hasattr(sys.modules[module_name], '__blueprints__'):
        existing_bps = getattr(sys.modules[module_name], '__blueprints__')
    else:
        existing_bps = {}

    existing_bps[bp_name] = bp
    setattr(sys.modules[module_name], '__blueprints__', existing_bps)

    return bp


def get_blueprint(bp_name: str, module_name: str) -> Blueprint:
    """
    Gets a blueprint registered for a plugin.
    Will throw an exception if the blueprint does not exist.

    :param bp_name: The blueprint name
    :param module_name: The module name of the **entry point** for the plugin, e.g. `plugins.base`
    :return: The blueprint
    """
    return getattr(sys.modules[module_name], '__blueprints__')[bp_name]


def add_column(model, column: database.db.Column):
    """
    Adds a column to an existing model.
    If the column exists already, nothing will happen.

    This function queues a direct SQL ALTER TABLE query,
    which will be executed once SQLAlchemy has created tables.

    :param model: The model
    :param column: An SQLAlchemy column instance
    """

    engine = database.db.engine
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)

    database.__queue_create_column__('ALTER TABLE %s ADD COLUMN %s %s' % (model.__tablename__, column_name, column_type))

    # model[column_name] = property(column)
    setattr(model, str(column_name), column)


def add_api_endpoints(model, methods: List[str],
                      include: list = None,
                      exclude: list = None,
                      page_size=250,
                      auth_func=None):
    database.__queue_api_endpoints__(database.APIEndpoint(model=model,
                                                          methods=methods,
                                                          include=include,
                                                          exclude=exclude,
                                                          page_size=page_size,
                                                          auth_func=auth_func))


def _load_modules():
    modules = settings.get_key('plugins')
    for module in modules:
        plugin = importlib.import_module('plugins.%s' % module)

        # Every plugin should have an init entry point
        plugin.init()

        if hasattr(sys.modules[plugin.__name__], '__blueprints__'):
            for bp in plugin.__blueprints__:
                server.app.register_blueprint(plugin.__blueprints__[bp])


def __start__():
    global logger
    logger = logging.getLogger(__name__)

    logger.debug('Loading plugins')
    _load_modules()
