from watchdog.observers import Observer
import logging
import settings
import os
import atexit

from plugins.base.television import Episode
from plugins.base.utils import MediaEventHandler
from .scanner import import_tv

logger: logging.Logger
observer: Observer


def watch_television():
    global observer
    global logger

    logger = logging.getLogger(__name__)

    path = os.path.expanduser(settings.get_key('plugins.base.tv.path'))

    logger.debug('Starting television filewatcher on \'%s\'' % path)

    event_handler = MediaEventHandler(path, import_tv, Episode)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()


@atexit.register
def unwatch_television():
    logger.debug('Stopping television filewatcher')
    observer.stop()

