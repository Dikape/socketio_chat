import os
import peewee_async

BASE_DIR = os.path.join(os.getcwd(), 'socket_app')

DATABASE = {
    'database': 'socket_db',
    'password': 'kasianpass',
    'user': 'kasian',
    'host': 'localhost',
}

database = peewee_async.PostgresqlDatabase(None)
database.init(**DATABASE)
database.set_allow_sync(False)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates'),]
STATIC_DIR = os.path.join(BASE_DIR, 'static')
