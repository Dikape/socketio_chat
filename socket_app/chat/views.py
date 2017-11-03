import aiohttp_jinja2
from aiohttp import web


@aiohttp_jinja2.template('index.html')
async def index(request):
    """Serve the client-side application."""
    return {'user': request.user}

