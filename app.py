import aiohttp_jinja2
import jinja2
import peewee_async
from aiohttp import web
from socket_app.chat.socket_handlers import sio

import settings
from routes import setup_routes
from middlewares import MIDDLWARES


def make_app():
    app = web.Application(middlewares=MIDDLWARES)

    # add app to socketio objects
    sio.attach(app)

    # database configs
    app.database = settings.database
    app.objects = peewee_async.Manager(app.database)

    # load all urls
    setup_routes(app)

    # configure async jinja
    jinja_env = aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIRS),
        context_processors=[aiohttp_jinja2.request_processor], )

    return app


if __name__ == '__main__':
    web.run_app(make_app())