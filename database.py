from sqlite3 import OperationalError
from typing import List, NamedTuple, Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from flask_restless import APIManager
import settings
import server
import logging

# import plugin_loader

db: SQLAlchemy = SQLAlchemy()
api_manager: APIManager

logger: logging.Logger


class APIEndpoint(NamedTuple):
    model: Any
    methods: List[str]
    include: List[str]
    exclude: List[str]
    page_size: int
    auth_func: Any


_column_queue: List[str] = []
_api_endpoints_queue: List[APIEndpoint] = []


def __queue_create_column__(sql: str):
    global _column_queue
    _column_queue.append(sql)


def __queue_api_endpoints__(endpoints: APIEndpoint):
    global _api_endpoints_queue
    _api_endpoints_queue.append(endpoints)


def __create_all__():
    global _column_queue
    global _api_endpoints_queue
    global api_manager

    logger.debug('Creating database tables')
    db.create_all()

    api_manager = APIManager(server.app, flask_sqlalchemy_db=db)

    # Merge extra columns
    for query in _column_queue:
        try:
            db.engine.execute(query)
            logger.debug('Added column using query \'%s\'' % query)
        except (OperationalError, SQLAlchemyOperationalError):
            pass

    # Create API endpoints
    for endpoint in _api_endpoints_queue:
        logger.debug('Creating API endpoints for \'%s\'' % endpoint.model.__tablename__)

        if endpoint.auth_func:
            preprocessors = dict(GET_RESOURCE=[endpoint.auth_func],
                                 GET_COLLECTION=[endpoint.auth_func],
                                 GET_RELATION=[endpoint.auth_func],
                                 GET_RELATED_RESOURCE=[endpoint.auth_func])
        else:
            preprocessors = {}

        api_manager.create_api(endpoint.model,
                               methods=endpoint.methods,
                               includes=endpoint.include,
                               exclude=endpoint.exclude,
                               page_size=endpoint.page_size,
                               max_page_size=1000,
                               allow_functions=True,
                               preprocessors=preprocessors)


def __start__():
    global logger
    logger = logging.getLogger(__name__)

    app = server.app

    logger.info('Connecting to database')

    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = settings.get_key('database')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
