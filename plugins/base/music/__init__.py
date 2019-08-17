from plugins.base.utils import auth_request
from .models import *
from .scanner import *
from .watcher import *


def init():
    import plugin_loader
    import settings
    import os

    settings_set = settings.SettingsSet('plugins.base.music')

    settings_set.register_key('enable', True)
    settings_set.register_key('path', os.path.expanduser('~/Music'))

    if settings_set.get_key('enable'):
        plugin_loader.add_api_endpoints(Artist, ['GET'], exclude=['tracks', 'albums'], auth_func=auth_request)
        plugin_loader.add_api_endpoints(Album, ['GET'], exclude=['tracks'], auth_func=auth_request)
        plugin_loader.add_api_endpoints(Track, ['GET'], exclude=['playlists'], auth_func=auth_request)
        plugin_loader.add_api_endpoints(Genre, ['GET'], exclude=['albums'], auth_func=auth_request)
        plugin_loader.add_api_endpoints(Playlist, ['GET'], auth_func=auth_request)

        watch_music()
