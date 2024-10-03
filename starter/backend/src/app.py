import os

from dotenv import load_dotenv
from flask import Flask

from starter.backend.src.models import setup_db
from starter.backend.src.flaskr import api
from flask_cors import CORS

load_dotenv()
db_username = os.environ["DB_USERNAME"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]
sqlalchemy_database_uri = f"postgresql+psycopg2://{db_username}:{db_password}@127.0.0.1:5432/{db_name}"


def create_app():
    """Application-factory pattern"""
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/v1.0/*": {"origins": "*"}})

    app.register_blueprint(api)
    setup_db(app, sqlalchemy_database_uri)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
