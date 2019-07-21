from watchdog.observers import Observer
import logging
import settings
import os
import atexit
from .scanner import import_track
from .models import Track
from plugins.base.utils import MediaEventHandler

logger: logging.Logger
observer: Observer


def watch_music():
    global observer
    global logger

    logger = logging.getLogger(__name__)

    path = os.path.expanduser(settings.get_key('plugins.base.music.path'))
    logger.debug('Starting music filewatcher on \'%s\'' % path)

    event_handler = MediaEventHandler(path, import_track, Track)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()


@atexit.register
def unwatch_music():
    logger.debug('Stopping music filewatcher')
    observer.stop()
