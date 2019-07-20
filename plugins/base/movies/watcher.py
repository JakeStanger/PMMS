from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import settings
import os
import atexit
import server
from database import db
from .scanner import import_movie
from .models import Movie

logger: logging.Logger
observer: Observer


class MoviesEventHandler(FileSystemEventHandler):
    library_path: str

    def __init__(self):
        self.library_path = os.path.expanduser(settings.get_key('plugins.base.movies.path'))

    def on_created(self, event):
        if event.is_directory:
            return

        path = event.src_path

        with server.app.app_context():
            import_movie(path)
            db.session.commit()

        logger.info('Imported new movie at \'%s\'' % path)

    def on_moved(self, event):
        if event.is_directory:
            return

        src_path = event.src_path
        dest_path = event.dest_path

        relative_path = src_path.replace('%s/' % self.library_path, '')

        with server.app.app_context():
            movie = db.session.query(Movie).filter_by(path=relative_path).first()

            if movie:
                movie.path = dest_path.replace('%s/' % self.library_path, '')
            else:
                import_movie(dest_path)

            db.session.commit()

        logger.info('Moved movie from \'%s\' to \'%s\'' % (src_path, dest_path))

    def on_modified(self, event):
        if event.is_directory:
            return

        full_path = event.src_path
        relative_path = full_path.replace('%s/' % self.library_path, '')

        with server.app.app_context():
            movie = db.session.query(Movie).filter_by(path=relative_path).first()
            import_movie(full_path, movie)
            db.session.commit()

        logger.info('Modified existing movie at \'%s\'' % full_path)

    def on_deleted(self, event):
        if event.is_directory:
            return

        full_path = event.src_path
        relative_path = full_path.replace('%s/' % self.library_path, '')

        with server.app.app_context():
            db.session.query(Movie).filter_by(path=relative_path).delete()
            db.session.commit()

        logger.info('Deleted movie at \'%s\'' % full_path)


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

