from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import settings
import os
import atexit
import server
from database import db
from .scanner import import_track
from .models import Track

logger: logging.Logger
observer: Observer


class MusicEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        path = event.src_path

        with server.app.app_context():
            import_track(path, settings.get_key('plugins.base.music.path'))
            db.session.commit()

        logger.info('Imported new track at \'%s\'' % path)

    def on_moved(self, event):
        if event.is_directory:
            return

        src_path = event.src_path
        dest_path = event.dest_path

        library_path = settings.get_key('plugins.base.music.path')
        relative_path = src_path.replace('%s/' % library_path, '')

        with server.app.app_context():
            track = db.session.query(Track).filter_by(path=relative_path).first()

            if track:
                track.path = dest_path.replace('%s/' % library_path, '')
            else:
                import_track(dest_path, library_path)

            db.session.commit()

        logger.info('Moved track from \'%s\' to \'%s\'' % (src_path, dest_path))

    def on_modified(self, event):
        if event.is_directory:
            return

        full_path = event.src_path
        library_path = settings.get_key('plugins.base.music.path')
        relative_path = full_path.replace('%s/' % library_path, '')

        with server.app.app_context():
            track = db.session.query(Track).filter_by(path=relative_path).first()
            import_track(full_path, library_path, track)
            db.session.commit()

        logger.info('Modified existing track at \'%s\'' % full_path)

    def on_deleted(self, event):
        if event.is_directory:
            return

        full_path = event.src_path
        library_path = settings.get_key('plugins.base.music.path')
        relative_path = full_path.replace('%s/' % library_path, '')

        with server.app.app_context():
            db.session.query(Track).filter_by(path=relative_path).delete()
            db.session.commit()

        logger.info('Deleted track at \'%s\'' % full_path)


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
