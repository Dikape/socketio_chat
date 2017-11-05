import socketio

mgr = socketio.AsyncRedisManager('redis://')
sio = socketio.AsyncServer(client_manager=mgr)


__all__ = ('connect',
           'message',
           'disconnect')


@sio.on('connect', namespace='/chat')
async def connect(sid, environ):
    request = environ.get('aiohttp.request')
    if request.user:
        await sio.emit('online', {'user': request.user.username}, namespace='/chat')


@sio.on('message', namespace='/chat')
async def message(sid, data):
    print("message ", data)
    await sio.emit('reply', data['message'], namespace='/chat', room=data['room'])


@sio.on('disconnect', namespace='/chat')
async def disconnect(sid):
    print('disconnect ', sid)


@sio.on('close_room', namespace='/chat')
def close_room(room):
    print("Room {0} has been deleted".format(room))
    sio.close_room(room=room, namespace='/chat')


@sio.on('enter_room', namespace='/chat')
def enter_room(sid, data):
    if data['room'] and sid:
        print(sio)
        print("User has entered to room {0}".format(data['room']))
        sio.enter_room(sid, room=data['room'], namespace='/chat')

