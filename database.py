from flask_sqlalchemy import SQLAlchemy
import settings
import server
import logging

db: SQLAlchemy = SQLAlchemy()
logger: logging.Logger


def __create_all__():
    logger.debug('Creating database tables')
    db.create_all()


def __start__():
    global logger
    logger = logging.getLogger(__name__)

    app = server.app

    logger.info('Connecting to database')

    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = settings.get_key('database')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
