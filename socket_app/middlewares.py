from aiohttp_session import get_session
from aiohttp import web

__all__ = ('user_middleware', )


@web.middleware
async def user_middleware(request, handler):
    from models import User
    request.session = await get_session(request)
    request.user = None
    user_id = request.session.get('user')
    if user_id is not None:
        request.user = await request.app.objects.get(User, id=user_id)
    response = await handler(request)
    return response
