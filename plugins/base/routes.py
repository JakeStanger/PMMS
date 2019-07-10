import logging
import plugin_loader

logger = logging.getLogger(__name__)

logger.debug('Base module routes loading')

users = plugin_loader.create_blueprint('users', '/users', 'plugins.base')


@users.route('/')
def base():
    return "Base endpoint! Loaded from %s " % __name__
