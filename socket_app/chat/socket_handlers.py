import socketio
import datetime

from peewee import JOIN
from .models import Message, User, Room

mgr = socketio.AsyncRedisManager('redis://127.0.0.1:6379')
sio = socketio.AsyncServer(client_manager=mgr)


class ChatNamespace(socketio.AsyncNamespace):
    def __init__(self, *args, **kwargs):
        self.max_message_id_for_sid = {}
        super().__init__(*args, **kwargs)

    def get_request(self, sid):
        environ = self.server.environ.get(sid)
        request = environ.get('aiohttp.request')
        return request

    def set_max_message_id(self, sid, id):
        if not self.max_message_id_for_sid.get(sid):
            self.max_message_id_for_sid[sid] = id

    async def on_connect(self, sid, environ):
        request = environ.get('aiohttp.request')
        room = environ['HTTP_REFERER'].split('/')[-1]
        if request.user:
            self.enter_room(sid, room=room)
            await self.emit('online', {'user': request.user.username}, room=room)

    async def on_message(self, sid, data):
        request = self.get_request(sid)
        message = {
            'text': data['message'],
            'author': request.user,
            'created_datetime': datetime.datetime.now().strftime("%d/%m/%y %H:%M"),
            'room': data.get('room')
        }

        await request.app.objects.create(Message, **message)
        message['author'] = request.user.username
        await self.emit('reply', message, room=data['room'])

    async def on_get_previous(self, sid, data):

        request = self.get_request(sid)
        room = data.get('room')
        page_num = data['limit_from']
        messages_number = int(data['messages_number'])
        message_id = self.max_message_id_for_sid.get(sid)
        condition =  Message.id<=message_id if message_id else Message.id>0
        messages = await request.app.objects.execute(
            Message.select(Message, Room, User).
                join(Room, JOIN.LEFT_OUTER).
                switch(Message).join(User, JOIN.LEFT_OUTER).
                where(Message.room==room, condition).
                paginate(page_num, paginate_by=messages_number)
        )

        if messages:
            self.set_max_message_id(sid, messages[0].id)
        messages = [mess.to_json() for mess in messages[::-1]]
        if messages:
            await self.emit('previous_messages', messages, room=sid)


sio.register_namespace(ChatNamespace('/chat'))
