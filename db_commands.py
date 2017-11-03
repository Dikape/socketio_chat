import argparse
import peewee_async

from socket_app.chat import models

from socket_app.settings import database


objects = peewee_async.Manager(database)


def create_tables():
    print('CREATE TABLES:')
    with objects.allow_sync():
        for name in models.__all__:
            current_class = getattr(models, name)
            current_class.create_table(True)
            print('create table for class {0}'.format(name))


def drop_tables():
    print('DROP TABLES:')
    with objects.allow_sync():
        for name in models.__all__:
            current_class = getattr(models, name)
            current_class.drop_table(fail_silently=True, cascade=True)
            print('droped table for class {0}'.format(name))


AVAILABLE_COMMANDS = {
    'createtables': create_tables,
    'droptables': drop_tables,
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provides functions to work with db.')
    parser.add_argument('command', choices=list(AVAILABLE_COMMANDS.keys()))
    command = parser.parse_args().command
    AVAILABLE_COMMANDS[command]()
