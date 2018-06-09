"""
App initilization logic.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config, get_logger


db = SQLAlchemy()


def create_app(config_name: str):
    """Creates a Flask app instance using one of predefined configs."""

    app = Flask(__name__)
    conf_obj = config[config_name]
    app.config.from_object(conf_obj)
    conf_obj.init_app(app)
    db.init_app(app)

    app.custom_logger = get_logger('main')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
