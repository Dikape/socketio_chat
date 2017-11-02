import views
import settings


def setup_routes(app):
    app.router.add_static('/static', settings.STATIC_DIR, name='static')
    app.router.add_get('/', views.index, name='index')
