import os
from logging.config import fileConfig

from flask import Flask
from flasgger import Swagger

from app.server import app, api
from app.database import db, ma
from app.routes import routes

template = {
  "swagger": "2.0",
  "info": {
    "title": "My API",
    "description": "API for my data",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "me@me.com",
      "url": "www.me.com",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
  "host": "mysite.com",  # overrides localhost:500
  "basePath": "/api",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}


def create_app():
    fileConfig('logging.cfg', disable_existing_loggers=False)

    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False
    connect_database(app)
    routes.register_routes(api)
    swagger = Swagger(app)

def connect_database(app: 'Flask'):
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/FoodDB'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_ECHO'] = True # para spam de sqlalchemy colocar el True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)
    return db