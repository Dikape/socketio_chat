import base64

from aiohttp import web
from aiohttp_session import session_middleware, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from chat.models import User

__all__ = ('user_middleware', )

# key for sessions
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)


@web.middleware
async def user_middleware(request, handler):

    request.session = await get_session(request)
    request.user = None
    user_id = request.session.get('user')
    if user_id is not None:
        request.user = await request.app.objects.get(User, id=user_id)
    response = await handler(request)
    return response


MIDDLWARES = [
    session_middleware(EncryptedCookieStorage(secret_key)),
    user_middleware
]