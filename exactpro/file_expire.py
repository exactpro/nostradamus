#!/usr/bin/python3.4


'''
/*******************************************************************************
* Copyright 2016-2019 Exactpro (Exactpro Systems Limited)
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
******************************************************************************/
'''


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
