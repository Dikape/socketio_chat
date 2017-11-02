import peewee
from settings import database

__all__ = ('User', 'Room', 'Message')


class BaseModel(peewee.Model):
    """base model"""
    class Meta:
        database = database


class User(BaseModel):
    username = peewee.CharField(max_length=20, null=False, index=True, unique=True)


class Room(BaseModel):
    pass


class Message(BaseModel):
    pass


