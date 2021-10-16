import logging
from dataclasses import dataclass
from typing import List, Dict

from flask import request
from webargs.flaskparser import FlaskParser
from marshmallow import fields, post_load, Schema, ValidationError
from werkzeug.exceptions import BadRequest

from app.validators.utils import validate_ids, validate_filters, validate_pagination_params, validate_sort_by_params, validate_fields
from app.models.ingredients import VALID_FOOD_GROUPS, VALID_STORAGE_TYPE

log = logging.getLogger(__name__)


VALID_FIELDS = {
    'id',
    'name',
    'food_group',
    'veggie_friendly',
    'storage',
    'expiration_time',
    'date_created',
    'last_updated'
}

VALID_FILTERS = {
    'eq': ['id', 'name', 'food_group', 'veggie_friendly', 'storage'],
    'ne': ['id', 'food_group', 'veggie_friendly', 'storage'],
    'ilike': ['name'],
    'notilike': ['name'],
    'startswith': ['name'],
    'between': ['date_created', 'expiration_time'],
    'ge': ['date_created', 'expiration_time'],
    'gt': ['date_created', 'expiration_time'],
    'le': ['date_created', 'expiration_time'],
    'lt': ['date_created', 'expiration_time']
}

FILTERS_DATA_TYPES = {
    'integer_values': ['id', 'expiration_time'],
    'real_values': [],
    'discrete_values': {
        'food_group': VALID_FOOD_GROUPS,
        'storage': VALID_STORAGE_TYPE},  # ToDo: pasar esto a una config
    'boolean_values': ['veggie_friendly'],
    'date_values': ['date_created']
}

MAX_MULTIGET_IDS = 20

@dataclass
class IngredientSearchQueryParam:
    offset: int
    limit: int
    ids: str
    sort_by: str
    str_sort: str
    asc: bool
    filters: List[Dict]
    fields: List[str]


class IngredientSearchQuery(Schema): ## Todo: ver diferencia de ma.Schema vs Schema
    offset = fields.Integer()
    limit = fields.Integer()
    ids = fields.List(fields.Integer(), allow_none=True)
    sort_by = fields.String(allow_none=True)
    str_sort = fields.Boolean(allow_none=True)
    asc = fields.Boolean(allow_none=True)
    filters = fields.List(fields.Dict(), allow_none=True)
    fields = fields.List(fields.String(), allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return IngredientSearchQueryParam(**data)


class IngredientSearchQueryParser(FlaskParser):
    def load_querystring(self, req, schema):
        return _validate_params(req, schema)

    def handle_error(self, error, req, schema, error_status_code, error_headers):
        raise BadRequest(error.messages)


def _validate_params(request: 'request', schema):
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    str_ids = request.args.get('ids')
    sort_by = request.args.get('sort_by')
    asc = request.args.get('asc')
    fields = request.args.get('fields')

    validated_params = {}
    # eq, ne, ge, le, gt, lt, between, ilike, notilike, startswith
    # https://flask-rest-jsonapi.readthedocs.io/en/latest/filtering.html#simple-filters what each one means

    # validate filters first, to initialize errors variable
    validated_params['filters'], errors = validate_filters(request, VALID_FILTERS, FILTERS_DATA_TYPES)

    # ToDo: validar el resto de paramétros a pesar de que si solo viene `ids` se ignora el resto de parámetros ?
    if str_ids:
        validated_params['ids'], error_msg = validate_ids(str_ids, MAX_MULTIGET_IDS)
        if error_msg:
            errors['ids'] = error_msg

    # validated offset and limit
    validated_params['offset'], validated_params['limit'], error_msg = validate_pagination_params(offset, limit)
    if error_msg:
        errors['pagination'] = error_msg

    # validate sort_by and asc
    if sort_by:
        str_columns = ['name', 'food_group', 'storage']
        numeric_columns = ['id', 'expiration_time']

        validated_params['sort_by'], \
        validated_params['str_sort'], \
        validated_params['asc'], \
        error_msg = validate_sort_by_params(sort_by, asc, str_columns, numeric_columns)
        if error_msg:
            errors['sorting'] = error_msg

    if fields is not None:
        validated_params['fields'], error_msg = validate_fields(fields, VALID_FIELDS)
        if error_msg:
            errors['fields'] = error_msg

    # raise exception if errors exists
    if errors:
        raise ValidationError(errors)

    params = ['offset', 'limit', 'ids', 'sort_by', 'str_sort', 'asc', 'filters', 'fields']
    return {param: validated_params[param] if param in validated_params else None for param in params}
