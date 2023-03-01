# Import Dependencies
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.urandom(12).hex()
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')