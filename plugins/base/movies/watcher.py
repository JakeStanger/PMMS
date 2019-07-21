from watchdog.observers import Observer
import logging
import settings
import os
import atexit
from .scanner import import_movie
from .models import Movie
from plugins.base.utils import MediaEventHandler

logger: logging.Logger
observer: Observer


def watch_movies():
    global observer
    global logger

    logger = logging.getLogger(__name__)

    path = os.path.expanduser(settings.get_key('plugins.base.movies.path'))
    logger.debug('Starting movies filewatcher on \'%s\'' % path)

    event_handler = MediaEventHandler(path, import_movie, Movie)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()


@atexit.register
def unwatch_movies():
    logger.debug('Stopping movies filewatcher')
    observer.stop()

