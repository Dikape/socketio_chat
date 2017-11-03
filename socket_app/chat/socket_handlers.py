import socketio

mgr = socketio.AsyncRedisManager('redis://')
sio = socketio.AsyncServer(client_manager=mgr)


__all__ = ('connect',
           'message',
           'disconnect')


@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)


@sio.on('chat message', namespace='/chat')
async def message(sid, data):
    print("message ", data)
    await sio.emit('reply', data, namespace='/chat')


@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)


@sio.on('close_room', namespace='/chat')
async def close_room(room):
    print("Room {0} has been deleted".format(room))
    await sio.close_room(room=room, namespace='/chat')


@sio.on('enter_room', namespace='/chat')
async def enter_room(sid, room):
    print("Room {0} has been deleted".format(room))
    await sio.enter_room(sid, room=room, namespace='/chat')


@sio.on('leave_room', namespace='/chat')
async def enter_room(sid, room):
    print("Room {0} has been deleted".format(room))
    await sio.leave_room(sid, room=room, namespace='/chat')
