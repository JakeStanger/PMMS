from plugins.base.utils import auth_request
from .models import *
from .scanner import *
from .watcher import *


def init():
    import plugin_loader
    import settings
    import os

    settings_set = settings.SettingsSet('plugins.base.tv')

    settings_set.register_key('enable', True)
    settings_set.register_key('path', os.path.expanduser('~/Television'))

    if settings_set.get_key('enable'):
        plugin_loader.add_api_endpoints(Show, ['GET'], exclude=['seasons', 'episodes'], auth_func=auth_request)
        plugin_loader.add_api_endpoints(Season, ['GET'], exclude=['show', 'episodes'], auth_func=auth_request)
        plugin_loader.add_api_endpoints(Episode, ['GET'], exclude=['show', 'season'], auth_func=auth_request)

        watch_television()
