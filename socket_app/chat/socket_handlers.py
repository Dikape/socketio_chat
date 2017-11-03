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