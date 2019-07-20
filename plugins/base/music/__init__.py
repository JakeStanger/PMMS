from .models import *
from .scanner import *
from .watcher import *


def init():
    import plugin_loader
    import settings
    import os

    settings.register_key('plugins.base.music.enable', True)
    settings.register_key('plugins.base.music.path', os.path.expanduser('~/Music'))

    if settings.get_key('plugins.base.music.enable'):
        plugin_loader.add_api_endpoints(Artist, ['GET'], exclude=['tracks', 'albums'])
        plugin_loader.add_api_endpoints(Album, ['GET'], exclude=['tracks'])
        plugin_loader.add_api_endpoints(Track, ['GET'], exclude=['playlists'])
        plugin_loader.add_api_endpoints(Genre, ['GET'], exclude=['albums'])
        plugin_loader.add_api_endpoints(Playlist, ['GET'])

        watch_music()
