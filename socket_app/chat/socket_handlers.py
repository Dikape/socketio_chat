import socketio

mgr = socketio.AsyncRedisManager('redis://')
sio = socketio.AsyncServer(client_manager=mgr)


__all__ = ('connect',
           'message',
           'disconnect')


@sio.on('connect', namespace='/chat')
async def connect(sid, environ):
    request = environ.get('aiohttp.request')
    url = request.url
    print(url)
    await sio.enter_room(sid=sid, room=id, namespace='/chat')
    if request.user:
        await sio.emit('online', {'user': request.user.username}, namespace='/chat')


@sio.on('message', namespace='/chat')
async def message(sid, data):
    print("message ", data)
    await sio.emit('reply', data, namespace='/chat', room='3b3e3908-1b48-49f2-b18d-6ce52f876fb0')


@sio.on('disconnect', namespace='/chat')
async def disconnect(sid):
    print('disconnect ', sid)


@sio.on('close_room', namespace='/chat')
async def close_room(room):
    print("Room {0} has been deleted".format(room))
    await sio.close_room(room=room, namespace='/chat')


@sio.on('enter_room', namespace='/chat')
async def enter_room(sid, room):
    print("Room {0} has been deleted".format(room))
    await sio.enter_room(sid, room=room, namespace='/chat')

#
# @sio.on('leave_room', namespace='/chat')
# async def enter_room(sid, room):
#     print("Room {0} has been deleted".format(room))
#     await sio.leave_room(sid, room=room, namespace='/chat')
