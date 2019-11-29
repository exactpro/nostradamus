#!/usr/bin/python3.5
from flask_bootstrap import Bootstrap
from flask_sessionstore import Session
from main.exceptions import IncorrectValueError
from os import urandom
from app import app, start_server

if __name__ == '__main__':
    from app import StemmedTfidfVectorizer
    try:
        SESSION_TYPE = 'filesystem'
        app.config['SECRET_KEY'] = urandom(12)
        app.config['ENV'] = 'development'
        app.config.from_object(__name__)
        Session(app)
        Bootstrap(app)
    except (FileNotFoundError, KeyError, SyntaxError, ValueError, IncorrectValueError) as error:
        print(error)
    finally:
       app.run(debug=False)