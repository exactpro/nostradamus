'''
*******************************************************************************
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
*******************************************************************************
'''


from ldap3 import Server, Connection, SUBTREE, ALL, core
import time
from redis import StrictRedis, exceptions
import os
import shutil
import configparser
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from pathlib import Path

from main.exceptions import LDAPError



def check_session():
    """ Checks session activity.

    Returns:
        Boolean value.   

    """
    return 'username' not in session or 'session_id' not in session


def is_session_expired():
    if 'expired' in dict(request.args).keys():
        if request.args['expired'] == '1':
            return False
        else:
            return True
    else:
        return True


config = configparser.ConfigParser()
config.read(str(Path(__file__).parents[1]) + '/extensions/' + 'connections.ini')


def check_user(username, password, domain_settings):
    """ Checks if the user is registered.

        Parameters:
            username (str): username;
            password (str): password;
            domain_settings (dict): domain' settings.

        Returns:
            Boolean value.

    """
    server = Server(domain_settings['ad_server'], get_info=ALL)
    conn = Connection(
        server,
        user=username +
        domain_settings['ad_domain_suffix'],
        password=password,
        auto_bind='NONE',
        version=3,
        authentication='SIMPLE',
        client_strategy='SYNC',
        auto_referrals=True,
        check_names=True,
        read_only=False,
        lazy=False,
        raise_exceptions=False)
    try:
        if not conn.bind():
            raise LDAPError('The username or password is incorrect')
        else:
            return True
    except core.exceptions.LDAPPasswordIsMandatoryError:
        raise LDAPError('The username or password is incorrect')


class User:
    def __init__(self, username='user', password=None):
        self.__username  = username
        self.__password = password
    
    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, username):
        self.__username = username
        return self.__username
    
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        self.__password = password
        return self.__password

    def authentificate_user(self, domain_settings):
        authentification = check_user(self.username, self.password, domain_settings)
        if not authentification:
            raise LDAPError('Access denied.')


# NOTE: use command redis-cli config set notify-keyspace-events KEA in console if it is first start
def event_handler(msg):
    # use the commented command below to track session's messages
    # print(msg['channel'] + '---' + msg['data'])
    if msg['data'] in ['del', 'expired']:
        if os.path.exists(os.path.abspath(os.curdir) + '/backup/' + msg['channel'].split(':')[2]):
            shutil.rmtree(os.path.abspath(os.curdir) + '/backup/' + msg['channel'].split(':')[2], ignore_errors=True)


def start_redis(other=None):
    try:
        r = StrictRedis(host='localhost', port=6379, db=0, password=config['REDIS']['redis_password'],
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


def remove_folder(path):
    for root, dirs, files in os.walk(path):
        if files:
            for file_name in files:
                os.chmod('{root}/{file_name}'.format(root=root, file_name=file_name), 0o664)
    shutil.rmtree(path)


def create_folder(path):
    os.makedirs(path)
    os.chmod(path, 0o775)

