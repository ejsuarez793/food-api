import logging
from dataclasses import dataclass
from typing import List, Dict

from flask import request
from webargs.flaskparser import FlaskParser
from marshmallow import fields, post_load, Schema, ValidationError
from werkzeug.exceptions import BadRequest

from app.validators.utils import validate_fields

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

@dataclass
class IngredientQueryParam:
    fields: List[str]


class IngredientQuery(Schema): ## Todo: ver diferencia de ma.Schema vs Schema
    fields = fields.List(fields.String(), allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return IngredientQueryParam(**data)


class IngredientQueryParser(FlaskParser):
    def load_querystring(self, req, schema):
        return _validate_params(req, schema)

    def handle_error(self, error, req, schema, error_status_code, error_headers):
        raise BadRequest(error.messages)


def _validate_params(request: 'request', schema):
    fields = request.args.get('fields')

    validated_params = {}
    errors = {}

    if fields is not None:
        validated_params['fields'], errors_msg = validate_fields(fields, VALID_FIELDS)
        if errors_msg:
            errors['fields'] = errors_msg

    # raise exception if errors exists
    if errors:
        raise ValidationError(errors)

    params = ['fields']
    return {param: validated_params[param] if param in validated_params else None for param in params}
