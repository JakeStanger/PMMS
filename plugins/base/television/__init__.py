from .models import *
from .scanner import *
from .watcher import *


def init():
    import plugin_loader
    import settings
    import os

    settings.register_key('plugins.base.tv.enable', True)
    settings.register_key('plugins.base.tv.path', os.path.expanduser('~/Television'))

    if settings.get_key('plugins.base.tv.enable'):
        plugin_loader.add_api_endpoints(Show, ['GET'], exclude=['seasons', 'episodes'])
        plugin_loader.add_api_endpoints(Season, ['GET'], exclude=['show', 'episodes'])
        plugin_loader.add_api_endpoints(Episode, ['GET'], exclude=['show', 'season'])

    watch_television()
