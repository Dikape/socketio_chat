import socketio
import datetime

mgr = socketio.AsyncRedisManager('redis://127.0.0.1:6379')
sio = socketio.AsyncServer(client_manager=mgr)


class ChatNamespace(socketio.AsyncNamespace):
    def __init__(self, *args, **kwargs):
        self.users_sid = {}
        super().__init__(*args, **kwargs)

    async def on_connect(self, sid, environ):
        request = environ.get('aiohttp.request')
        room = environ['HTTP_REFERER'].split('/')[-1]
        if request.user:
            self.users_sid[sid] = request.user
            self.enter_room(sid, room=room)
            await self.emit('online', {'user': request.user.username}, room=room)

    async def on_message(self, sid, data):
        message = {
            'text': data['message'],
            'user': self.users_sid[sid].username,
            # 'time': datetime.datetime.now().time()

        }
        await self.emit('reply', message, room=data['room'])

    # def on_disconnect(self, sid):
    #     print('disconnect ', sid)

    # def on_enter_room(self, sid, data):
    #     if data['room'] and sid:
    #         print(data['room'] + '----room')
    #         # # print(sio)
    #         # print("User has entered to room {0}".format(data['room']))


    # def on_close_room(self, room):
    #     # print("Room {0} has been deleted".format(room))
    #     self.close_room(room=room)


sio.register_namespace(ChatNamespace('/chat'))