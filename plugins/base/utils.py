import re

from flask import request
from flask_login import current_user

import server
import logging
from database import db
from watchdog.events import FileSystemEventHandler
from .users.routes import load_user_from_request

from flask_restless import ProcessingException


def get_name_sort(name: str):
    if not name:
        return None
    return re.match('^(?:The |A )?(.*)', name)[1]


def auth_request(**kw):
    if not current_user.is_authenticated:
        user = load_user_from_request(request)
        if not user:
            raise ProcessingException(description='Not Authorized', status=401)


class MediaEventHandler(FileSystemEventHandler):
    library_path: str

    def __init__(self, library_path: str, import_func, model):
        self.library_path = library_path
        self.import_func = import_func
        self.model = model
        self.logger = logging.getLogger(__name__)

    def on_created(self, event):
        if event.is_directory:
            return

        path = event.src_path

        with server.app.app_context():
            self.import_func(path)
            db.session.commit()

        self.logger.info('Imported new %s at \'%s\'' % (self.model.__name__, path))

    def on_moved(self, event):
        if event.is_directory:
            return

        src_path = event.src_path
        dest_path = event.dest_path

        relative_path = src_path.replace('%s/' % self.library_path, '')

        with server.app.app_context():
            track = db.session.query(self.model).filter_by(path=relative_path).first()

            if track:
                track.path = dest_path.replace('%s/' % self.library_path, '')
            else:
                self.import_func(dest_path)

            db.session.commit()

        self.logger.info('Moved %s from \'%s\' to \'%s\'' % (self.model.__name__, src_path, dest_path))

    def on_modified(self, event):
        if event.is_directory:
            return

        full_path = event.src_path
        relative_path = full_path.replace('%s/' % self.library_path, '')

        with server.app.app_context():
            track = db.session.query(self.model).filter_by(path=relative_path).first()
            self.import_func(full_path, track)
            db.session.commit()

        self.logger.info('Modified existing %s at \'%s\'' % (self.model.__name__, full_path))

    def on_deleted(self, event):
        if event.is_directory:
            return

        full_path = event.src_path
        relative_path = full_path.replace('%s/' % self.library_path, '')

        with server.app.app_context():
            db.session.query(self.model).filter_by(path=relative_path).delete()
            db.session.commit()

        self.logger.info('Deleted %s at \'%s\'' % (self.model.__name__, full_path))
