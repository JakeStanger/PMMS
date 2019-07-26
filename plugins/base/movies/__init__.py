from plugins.base.utils import auth_request
from .models import *
from .scanner import *
from .watcher import *


def init():
    import plugin_loader
    import settings
    import os

    settings.register_key('plugins.base.movies.enable', True)
    settings.register_key('plugins.base.movies.path', os.path.expanduser('~/Movies'))

    if settings.get_key('plugins.base.movies.enable'):
        plugin_loader.add_api_endpoints(Movie, ['GET'], auth_func=auth_request)

        watch_movies()
