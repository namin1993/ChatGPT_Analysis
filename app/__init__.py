from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
from flask_login import LoginManager
import yagmail
import keyring
import keyrings.alt
import os

# Initialization
app = Flask(__name__)
app.config.from_object(Config)

# SQLAlchemy Engine
db = SQLAlchemy(app)
migrate = Migrate(app, db)

DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(DB_URI)

# Setup email
EMAIL_ACCOUNT = app.config['EMAIL_ACCOUNT']
EMAIL_API_KEY = app.config['EMAIL_API_KEY']
keyring.set_password("yagmail", str(EMAIL_ACCOUNT), str(EMAIL_API_KEY))
keyring.get_password(str(EMAIL_ACCOUNT))

# Flask-login
login = LoginManager(app)
login.login_view = 'login'

from app import routes