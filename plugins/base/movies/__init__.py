from plugins.base.utils import auth_request
from .models import *
from .scanner import *
from .watcher import *


def init():
    import plugin_loader
    import settings
    import os

    settings_set = settings.SettingsSet('plugins.base.movies')

    settings_set.register_key('enable', True)
    settings_set.register_key('path', os.path.expanduser('~/Movies'))

    if settings_set.get_key('enable'):
        plugin_loader.add_api_endpoints(Movie, ['GET'], auth_func=auth_request)

        watch_movies()
