from sqlite3 import OperationalError
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import  OperationalError as SQLAlchemyOperationalError
import settings
import server
import logging

db: SQLAlchemy = SQLAlchemy()
logger: logging.Logger


_column_queue: List[str] = []


def __queue_create_column__(sql: str):
    global _column_queue
    _column_queue.append(sql)


def __create_all__():
    global _column_queue

    logger.debug('Creating database tables')
    db.create_all()

    for query in _column_queue:
        try:
            db.engine.execute(query)
        except (OperationalError, SQLAlchemyOperationalError):
            pass


def __start__():
    global logger
    logger = logging.getLogger(__name__)

    app = server.app

    logger.info('Connecting to database')

    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = settings.get_key('database')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
