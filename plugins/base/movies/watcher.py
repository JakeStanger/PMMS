from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import settings
import os
import atexit
import server
from database import db

logger: logging.Logger
observer: Observer


class MoviesEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        pass

    def on_moved(self, event):
        pass

    def on_modified(self, event):
        pass

    def on_deleted(self, event):
        pass


def watch_movies():
    global observer
    global logger

    logger = logging.getLogger(__name__)

    path = os.path.expanduser(settings.get_key('plugins.base.movies.path'))

    logger.debug('Starting movies filewatcher on \'%s\'' % path)

    event_handler = MoviesEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()


@atexit.register
def unwatch_movies():
    logger.debug('Stopping movies filewatcher')
    observer.stop()

