from flask import Flask
from flask_script import Manager, Server as BaseServer

import server
import settings
import database
import plugin_loader
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Server(BaseServer):
    def __call__(self, app, *args, **kwargs):
        settings.__start__()
        database.__start__()

        plugin_loader.__start__()

        app.secret_key = settings.get_key('secret_key')

        # These should always be the last things to init, in this order
        database.__create_all__()

        return BaseServer.__call__(self, app, *args, **kwargs)


app = Flask(__name__)


app.app_context().push()

# lazy way of avoiding circular references
server.app = app

manager = Manager(app)
manager.add_command('runserver', Server())

if __name__ == '__main__':
    manager.run()

