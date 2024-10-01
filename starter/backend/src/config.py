import os
from dotenv import load_dotenv

SECRET_KEY = os.urandom(32)
load_dotenv()

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
db_username = os.environ["DB_USERNAME"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{db_username}:{db_password}@127.0.0.1:5432/{db_name}"


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
