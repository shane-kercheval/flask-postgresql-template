import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from config import DevelopmentConfig


print("#############################")
app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', DevelopmentConfig))
app.secret_key = app.config['SECRET_KEY']
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
