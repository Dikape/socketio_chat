import aiohttp_jinja2
from aiohttp import web

from models import User, Room

@aiohttp_jinja2.template('index.html')
async def index(request):
    """Serve the client-side application."""
    all_objects = await request.app.objects.execute(Room.select())
    return {'user': request.user, 'chats': all_objects}


@aiohttp_jinja2.template('chat.html')
async def chat(request):
    id = request.match_info['id']
    if request.user:
        try:
            chat = await request.app.objects.get(Room, id=id)
        except:
            raise web.HTTPNotFound
        return {'chat': chat}
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


async def create_chat(request):
    data = await request.post()
    title = data['chat_title']
    chat, created = await request.app.objects.get_or_create(Room, title=title)
    # if not created:
    #     raise web.HTTPConflict
    url = request.app.router['index'].url_for()
    return web.HTTPFound(url)