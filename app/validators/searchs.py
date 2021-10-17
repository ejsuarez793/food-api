import logging
from dataclasses import dataclass
from typing import List, Dict

from flask import request
from webargs.flaskparser import FlaskParser
from marshmallow import fields, post_load, Schema, ValidationError
from werkzeug.exceptions import BadRequest

from app.validators.utils import validate_ids, validate_filters, validate_pagination_params, validate_sort_by_params, validate_fields

log = logging.getLogger(__name__)


@dataclass
class SearchQueryParam:
    offset: int
    limit: int
    ids: str
    sort_by: str
    str_sort: str
    asc: bool
    filters: List[Dict]
    fields: List[str]
    fields_ingredients: List[str]


class SearchQuery(Schema): ## Todo: ver diferencia de ma.Schema vs Schema
    offset = fields.Integer()
    limit = fields.Integer()
    ids = fields.List(fields.Integer(), allow_none=True)
    sort_by = fields.String(allow_none=True)
    str_sort = fields.Boolean(allow_none=True)
    asc = fields.Boolean(allow_none=True)
    filters = fields.List(fields.Dict(), allow_none=True)
    fields_ingredients = fields.List(fields.String(), allow_none=True)
    fields = fields.List(fields.String(), allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return SearchQueryParam(**data)


class SearchQueryParser(FlaskParser):

    # ToDo: crear una clase hija que se encargue de leer y asignar solamente estos attributos
    def __init__(self,
                 valid_filters=None,
                 filters_data_types=None,
                 max_multiget_ids=20,
                 max_limit=10,
                 str_columns=None,
                 numeric_columns=None,
                 valid_fields=None,
                 valid_fields_ingredients=None):

        self.valid_filters = valid_filters
        self.filters_data_types = filters_data_types
        self.max_multiget_ids = max_multiget_ids
        self.max_limit = max_limit
        self.str_columns = str_columns
        self.numeric_columns = numeric_columns
        self.valid_fields = valid_fields
        self.valid_fields_ingredients = valid_fields_ingredients

        self.is_offset_and_limit_validation_on = self.max_limit is not None
        self.is_filters_validation_on = self.valid_filters is not None and self.filters_data_types is not None
        self.is_multiget_length_validation_on = self.max_multiget_ids is not None
        self.is_sort_validation_on = self.str_columns is not None and self.numeric_columns is not None
        self.is_fields_validation_on = self.valid_fields is not None
        self.is_fields_ingredients_validation_on = self.valid_fields_ingredients is not None
        super().__init__()

    def load_querystring(self, req, schema):
        return self._validate_params(req, schema)

    def handle_error(self, error, req, schema, error_status_code, error_headers):
        raise BadRequest(error.messages)

    def _validate_params(self, request: 'request', schema):
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        str_ids = request.args.get('ids')
        sort_by = request.args.get('sort_by')
        asc = request.args.get('asc')
        fields = request.args.get('fields')
        fields_ingredients = request.args.get('fields_ingredients')

        validated_params = {}
        errors = {}
        # eq, ne, ge, le, gt, lt, between, ilike, notilike, startswith
        # https://flask-rest-jsonapi.readthedocs.io/en/latest/filtering.html#simple-filters what each one means

        # validate filters first, to initialize errors variable
        if self.is_filters_validation_on:
            validated_params['filters'], errors = validate_filters(request, self.valid_filters, self.filters_data_types)

        if self.is_multiget_length_validation_on and str_ids:
            validated_params['ids'], error_msg = validate_ids(str_ids, self.max_multiget_ids)
            if error_msg:
                errors['ids'] = error_msg

        # validated offset and limit
        if self.is_offset_and_limit_validation_on:
            validated_params['offset'], validated_params['limit'], error_msg = validate_pagination_params(offset, limit, self.max_limit)
            if error_msg:
                errors['pagination'] = error_msg

        # validate sort_by and asc
        if self.is_sort_validation_on and sort_by:
            str_columns = self.str_columns
            numeric_columns = self.numeric_columns

            validated_params['sort_by'], \
            validated_params['str_sort'], \
            validated_params['asc'], \
            error_msg = validate_sort_by_params(sort_by, asc, str_columns, numeric_columns)
            if error_msg:
                errors['sorting'] = error_msg

        if self.is_fields_validation_on and fields is not None:
            validated_params['fields'], error_msg = validate_fields(fields, self.valid_fields)
            if error_msg:
                errors['fields'] = error_msg

        if self.is_fields_ingredients_validation_on and fields_ingredients is not None:
            validated_params['fields_ingredients'], errors_msg = validate_fields(fields_ingredients, self.valid_fields_ingredients)
            if errors_msg:
                errors['fields_ingredients'] = errors_msg

        # raise exception if errors exists
        if errors:
            raise ValidationError(errors)

        params = ['offset', 'limit', 'ids', 'sort_by', 'str_sort', 'asc', 'filters', 'fields', 'fields_ingredients']
        return {param: validated_params[param] if param in validated_params else None for param in params}