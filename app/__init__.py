"""
This module starts up the application:
    1) Set ups logging config
    2) connects to the PostgreSQL database
    3) Register routes
"""

from logging.config import fileConfig

from flask import Flask
from flask_restx import Api
from app.database import db
from app.database import ma
from app.routes import routes


def create_app():
    """
    This function initialize the flask app
    :return: Flask application object
    """
    fileConfig('logging.cfg', disable_existing_loggers=False)

    app = Flask(__name__)
    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False
    connect_database(app)
    api = Api(app)
    routes.register_routes(api)
    return app


def connect_database(app: 'Flask'):
    """
    This function connects to the database, currently using postgres
    :param app: Flask application object
    :return: Flask alchemy object
    """

    app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] = 'postgresql://postgres:postgres@localhost/FoodDB'
    app.config[
        'SQLALCHEMY_ECHO'
    ] = False  # para spam de sqlalchemy colocar el True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)
    return db
