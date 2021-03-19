import logging
import datetime
from dataclasses import dataclass

from flask import request
from webargs.flaskparser import FlaskParser
from marshmallow import fields, post_load, Schema, ValidationError
from werkzeug.exceptions import BadRequest

log = logging.getLogger(__name__)


@dataclass
class RecipeQueryParams:
    offset: int
    limit: int
    date_from: str
    date_to: str


class RecipeSearchQuery(
    Schema
):  ## Todo: ver diferencia de ma.Schema vs Schema
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

    def handle_error(
        self, error, req, schema, error_status_code, error_headers
    ):
        raise BadRequest(error.messages)


def _validate_params(request: 'request', schema):
    str_date_to = request.args.get('date_to')
    str_date_from = request.args.get('date_from')
    offset = request.args.get('offset')
    limit = request.args.get('limit')

    dateParamsAvailable = (
        str_date_from is not None and str_date_to is not None
    )
    try:
        offset = int(offset) if offset is not None else 0
        limit = int(limit) if limit is not None else 10
        if dateParamsAvailable:
            date_from = datetime.datetime.strptime(str_date_from, '%Y-%m-%d')
            date_to = datetime.datetime.strptime(str_date_to, '%Y-%m-%d')
    except Exception as e:
        log.error(
            'there was an error parsing params [error:{}]'.format(str(e))
        )
        raise ValidationError(
            'there was an error parsing params. please check data types'
        )

    errors = {}
    if dateParamsAvailable and date_from > date_to:
        errors[
            'date_from'
        ] = 'param \'date_from\' cant be greater than \'date_to\''

    # we do not raise error for bad limit and offset params, we adjust them
    offset = 0 if offset < 0 else offset
    limit = 10 if limit <= 0 or limit > 10 else limit

    if errors:
        raise ValidationError(errors)

    return dict(
        {
            'offset': offset,
            'limit': limit,
            'date_from': str_date_from,
            'date_to': str_date_to,
        }
    )
