# Import Dependencies
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #SECRET_KEY = os.urandom(12).hex()
    SECRET_KEY = 'some-secret-key-1234'
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = uri
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')