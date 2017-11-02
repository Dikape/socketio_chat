import base64
import peewee_async

from cryptography import fernet
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from middlewares import user_middleware

DATABASE = {
    'database': 'socket_db',
    'password': 'kasianpass',
    'user': 'kasian',
    'host': 'localhost',
}

database = peewee_async.PostgresqlDatabase(None)
database.init(**DATABASE)
database.set_allow_sync(False)

# key for sessions
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)


MIDDLWARES = [
    session_middleware(EncryptedCookieStorage(secret_key)),
    user_middleware
]

TEMPLATE_DIRS = ['templates',]
STATIC_DIR = 'static'
