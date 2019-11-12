#!/usr/bin/python3.5
from flask_bootstrap import Bootstrap
from flask_redisSession import RedisSession
from flask_sessionstore import Session
from main.config_processor import Configuration
from configparser import ConfigParser
from main.exceptions import IncorrectValueError
from datetime import timedelta
import os
from pathlib import Path
from main.data_analysis import run_in_parallel
from ast import literal_eval


from app import app, start_server
from main.session import start_redis

if __name__ == '__main__':
    from app import StemmedTfidfVectorizer
    try:
        inner = literal_eval(Configuration('config.ini').get_settings()['APP']['version'])
        if int(inner) not in (0, 1):
            raise IncorrectValueError('Please use only 0 or 1 values for inner parameter in config.ini')
        # setting up session
        if int(inner) == 1: # for company needs only (session stored to redis)
            config_reader = Configuration(str(Path(__file__).parents[0]) + '/extensions/' + 'connections.ini')
            SESSION_TYPE = 'redis'
            PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # minutes=30 seconds=10
            REDIS_PASSWORD = config_reader.get_settings()['REDIS']['redis_password']
            app.config['USE_SECRET_KEY'] = False
        else:
            SESSION_TYPE = 'filesystem' # FOR OPENSOURCE NEEDS (session stored to HDD)
            app.config['SECRET_KEY'] = os.urandom(12)
        app.config['ENV'] = 'development'
            
        # Flask setting up
        app.config.from_object(__name__)
        RedisSession(app) if int(inner) == 1 else Session(app)
        Bootstrap(app)
        
    except (FileNotFoundError, KeyError, SyntaxError, ValueError, IncorrectValueError) as error:
        print(str(error))

    else:
        if int(inner) == 1:
            run_in_parallel(flask=start_server, redis_expire=start_redis)
        else:
            app.run(debug=False)
    app.run(debug=False)