from starter.backend.src.config import Config
from starter.backend.src.models import setup_db
from starter.backend.src.flaskr import app

config = Config()


def create_app():
    """Application-factory pattern"""
    setup_db(app, config)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000)
