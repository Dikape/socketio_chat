import settings

from chat.urls import routes as chat_routes


def setup_routes(app):
    app.router.add_static('/static', settings.STATIC_DIR, name='static')
    for route in chat_routes:
        app.router.add_route(**route)
