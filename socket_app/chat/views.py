import aiohttp_jinja2
from aiohttp import web

from models import User

@aiohttp_jinja2.template('index.html')
async def index(request):
    """Serve the client-side application."""
    return {'user': request.user}


@aiohttp_jinja2.template('chat.html')
async def chat(request):
    id = request.match_info['id']
    if request.user:
        return {'id': id}
    else:
        raise web.HTTPForbidden


async def login_user(request, user):
    request.session['user'] = str(user.id)


async def login(request):
    data = await request.post()
    username = data['username']
    password = data['password']
    user, create = await request.app.objects.create_or_get(
        User, username=username,
        password=password)
    await login_user(request, user)
    url = request.app.router['index'].url_for()
    return web.HTTPFound(url)

