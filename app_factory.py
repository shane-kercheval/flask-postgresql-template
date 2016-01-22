import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', DevelopmentConfig))
app.secret_key = app.config['SECRET_KEY']

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u'Please log in to access this page.'
login_manager.login_message_category = 'error'
