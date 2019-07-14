from sqlite3 import OperationalError
from typing import List, Dict, NamedTuple, Any

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
    include_columns: List[str]
    exclude_columns: List[str]


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
        api_manager.create_api(endpoint.model, methods=endpoint.methods,
                               include_columns=endpoint.include_columns,
                               exclude_columns=endpoint.exclude_columns)


def __start__():
    global logger
    logger = logging.getLogger(__name__)

    app = server.app

    logger.info('Connecting to database')

    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = settings.get_key('database')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
