from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import settings
import os
import atexit
import server
from database import db
from .scanner import import_track

logger: logging.Logger
observer: Observer


class MusicEventHandler(FileSystemEventHandler):
    def on_moved(self, event):
        logger.debug(event)

    def on_created(self, event):
        logger.debug(event)

        if event.is_directory:
            return

        path = event.src_path

        with server.app.app_context():
            import_track(path, settings.get_key('plugins.base.music.path'))
            db.session.commit()

        logger.info('Imported new track at \'%s\'' % path)

    def on_deleted(self, event):
        logger.debug(event)

    def on_modified(self, event):
        logger.debug(event)


def watch_music():
    global observer
    global logger

    logger = logging.getLogger(__name__)

    path = os.path.expanduser(settings.get_key('plugins.base.music.path'))

    logger.debug('Starting music filewatcher on \'%s\'' % path)

    event_handler = MusicEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()


@atexit.register
def unwatch_music():
    logger.debug('Stopping music filewatcher')
    observer.stop()
