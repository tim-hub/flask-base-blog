from flask import Flask
# import config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config') # load config.py from root folder
app.config.from_pyfile('config.py')  # load from instance folder
COOKIE_SALT= app.config['COOKIE_SALT']

from blog_base import *