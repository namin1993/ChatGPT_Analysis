# Import Dependencies
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #SECRET_KEY = os.urandom(12).hex()

    SECRET_KEY = os.environ.get("SECRET_KEY", "development-secret-key")
    EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
    EMAIL_API_KEY = os.getenv("EMAIL_PASSWORD")
    uri = os.getenv("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri or "sqlite:///app.db"
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')