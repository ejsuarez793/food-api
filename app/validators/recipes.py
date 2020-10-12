from dataclasses import dataclass

from flask import request
from webargs.flaskparser import FlaskParser
from marshmallow import fields, post_load, Schema
from app.utils.utils import validate_dates, validate_offset, validate_limit

@dataclass
class RecipeQueryParams:
    offset: int
    limit: int
    date_from: str
    date_to: str


class RecipeSearchQuery(Schema): ## Todo: ver diferencia de ma.Schema vs Schema
    offset = fields.Integer()
    limit = fields.Integer()
    date_to = fields.String()
    date_from = fields.String()

    @post_load
    def make_object(self, data, **kwargs):
        return RecipeQueryParams(**data)


class RecipeSearchQueryParser(FlaskParser):
    def load_querystring(self, req, schema):
        return _validate_params(req, schema)


def _validate_params(request: 'request', schema):
    date_to = request.args.get('date_to')
    date_from = request.args.get('date_from')

    if date_to is not None and date_from is not None:
        validate_dates(date_from, date_to)

    offset = request.args.get('offset')
    limit = request.args.get('limit')
    offset = validate_offset(offset)
    limit = validate_limit(limit)

    return dict({'offset': offset, 'limit': limit, 'date_from': date_from, 'date_to': date_to})
