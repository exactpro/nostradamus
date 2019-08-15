#!/usr/bin/python3.4

import time
from redis import StrictRedis, exceptions
import os
import shutil
import configparser


config = configparser.ConfigParser()
config.read('myconf.ini')


# NOTE: use command redis-cli config set notify-keyspace-events KEA in console if it is first start
def event_handler(msg):
    # use the commented command below to track session's messages
    # print(msg['channel'] + '---' + msg['data'])
    if msg['data'] in ['del', 'expired']:
        if os.path.exists(os.path.abspath(os.curdir) + '/files/' + msg['channel'].split(':')[2]):
            shutil.rmtree(os.path.abspath(os.curdir) + '/files/' + msg['channel'].split(':')[2], ignore_errors=True)


def start(other=None):
    try:
        r = StrictRedis(host='localhost', port=6379, db=0, password=config['Path']['redis_password'],
                         charset="utf-8", decode_responses=True)
        pubsub = r.pubsub()
        pubsub.psubscribe(**{'__keyspace@0__:*': event_handler})
        while True:
            message = pubsub.get_message()
            if message:
                pass
            else:
                time.sleep(0.01)
    except exceptions.ConnectionError as e:
        if other:
            print('Redis: {}'.format(e))
            other.terminate()

