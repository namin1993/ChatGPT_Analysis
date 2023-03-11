from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
from flask_login import LoginManager
import os

# Initialization
app = Flask(__name__)
app.config.from_object(Config)

# Migration directory
MIGRATION_DIR = os.path.join('app', 'migrations')

# SQLAlchemy Engine
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATION_DIR)

DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(DB_URI)

# Flask-login
login = LoginManager(app)
login.login_view = 'login'

from app import routes