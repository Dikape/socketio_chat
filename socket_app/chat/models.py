import uuid
import peewee

from datetime import datetime
from socket_app.settings import database

__all__ = ('User', 'Room', 'Message')


class BaseModel(peewee.Model):
    """base model"""
    class Meta:
        database = database


class User(BaseModel):
    username = peewee.CharField(max_length=20, null=False, index=True, unique=True)
    password = peewee.CharField(max_length=100, null=False)

    def __str__(self):
        return self.username


class Room(BaseModel):
    id = peewee.UUIDField(default=uuid.uuid4, primary_key=True)
    title = peewee.CharField(max_length=50, null=False)
    created_datetime = peewee.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class UserRoom(BaseModel):
    user = peewee.ForeignKeyField(User, related_name='chats')
    room = peewee.ForeignKeyField(Room, related_name='members')


class Message(BaseModel):
    text = peewee.CharField(max_length=200, null=False)
    author = peewee.ForeignKeyField(User)
    room = peewee.ForeignKeyField(Room)
    created_datetime = peewee.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.text
