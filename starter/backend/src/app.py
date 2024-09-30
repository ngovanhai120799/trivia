from starter.backend.src.config import config, CONFIG_MODE
from starter.backend.src.models import setup_db
from starter.backend.src.flaskr import app


def create_app():
    """Application-factory pattern"""
    config_mode = config[CONFIG_MODE]
    app.config.from_object(config_mode)
    setup_db(app, config_mode)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000)
