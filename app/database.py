"""
Simple module that starts SQLAlchemy db object and Marshmallow object
to be able to import them in other modules
"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
