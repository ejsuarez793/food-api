import logging
import datetime
from dataclasses import dataclass
from typing import List

from flask import request
from webargs.flaskparser import FlaskParser
from marshmallow import fields, post_load, Schema, ValidationError
from werkzeug.exceptions import BadRequest

log = logging.getLogger(__name__)

from app.validators.utils import validate_ids, validate_date_range, validate_pagination_params, validate_sort_by_params

@dataclass
class IngredientQueryParam:
    offset: int
    limit: int
    date_from: str
    date_to: str
    name: str
    ids: str
    sort_by: str
    str_sort: str
    asc: bool
    # filters: List[str] #ToDo: implementar luego


class IngredientSearchQuery(Schema): ## Todo: ver diferencia de ma.Schema vs Schema
    offset = fields.Integer()
    limit = fields.Integer()
    date_to = fields.String(allow_none=True)
    date_from = fields.String(allow_none=True)
    name = fields.String(allow_none=True)
    ids = fields.List(fields.Integer(), allow_none=True)
    sort_by = fields.String(allow_none=True)
    str_sort = fields.Boolean(allow_none=True)
    asc = fields.Boolean(allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return IngredientQueryParam(**data)


class IngredientQueryParser(FlaskParser):
    def load_querystring(self, req, schema):
        return _validate_params(req, schema)

    def handle_error(self, error, req, schema, error_status_code, error_headers):
        raise BadRequest(error.messages)


def _validate_params(request: 'request', schema):
    str_date_to = request.args.get('date_to')
    str_date_from = request.args.get('date_from')
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    name = request.args.get('name')
    str_ids = request.args.get('ids')
    sort_by = request.args.get('sort_by')
    asc = request.args.get('asc')

    validated_params = {}
    errors = {}

    date_params_available = str_date_from is not None and str_date_to is not None
    if date_params_available:
        validated_params['date_to'], validated_params['date_from'], error_msg = validate_date_range(str_date_to, str_date_from)
        if error_msg:
            errors['date_range'] = error_msg

    if str_ids:
        validated_params['ids'], error_msg = validate_ids(str_ids)
        if error_msg:
            errors['ids'] = error_msg

    # validated offset and limit
    validated_params['offset'], validated_params['limit'], error_msg = validate_pagination_params(offset, limit)
    if error_msg:
        errors['pagination'] = error_msg

    # validate sort_by and asc
    str_columns = ['name', 'food_group', 'storage']
    numeric_columns = ['id', 'price', 'expiration_time']

    validated_params['sort_by'], \
    validated_params['str_sort'], \
    validated_params['asc'], \
    error_msg = validate_sort_by_params(sort_by, asc, str_columns, numeric_columns)
    if error_msg:
        errors['sorting'] = error_msg

    # validate name
    validated_params['name'] = name

    # raise exception if errors exists
    if errors:
        raise ValidationError(errors)

    params = ['date_to', 'date_from', 'offset', 'limit', 'name', 'ids', 'sort_by', 'str_sort', 'asc']
    return {param: validated_params[param] if param in validated_params else None for param in params}
