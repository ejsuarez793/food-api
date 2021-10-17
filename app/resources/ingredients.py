from flask import request, make_response
from flask_restx import Resource

from marshmallow import RAISE
from app.repositories import ingredients

from app.validators.searchs import SearchQuery, SearchQueryParser, SearchQueryParam

from app.validators.ingredients_search import VALID_FIELDS_FOR_SEARCH, \
    VALID_FILTERS, FILTERS_DATA_TYPES, STR_COLUMNS, NUMERIC_COLUMNS


search_query_parser = SearchQueryParser(valid_filters=VALID_FILTERS,
                                        filters_data_types=FILTERS_DATA_TYPES,
                                        str_columns=STR_COLUMNS,
                                        numeric_columns=NUMERIC_COLUMNS,
                                        valid_fields=VALID_FIELDS_FOR_SEARCH)

fields_query_parser = SearchQueryParser(valid_fields=VALID_FIELDS_FOR_SEARCH)


class Ingredient(Resource):

    @search_query_parser.use_args(SearchQuery(unknown=RAISE), location='query')
    def get(self, params: 'SearchQueryParam'):
        response, error = ingredients.search(params)
        if error:
            return error, error['status_code']
        return response, 200

    def post(self):
        json_data = request.get_json()
        response, err = ingredients.create(json_data)
        if err:
            return make_response(err, err['status_code'])
        return make_response(response, 201)


class IngredientById(Resource):

    @fields_query_parser.use_args(SearchQuery(unknown=RAISE), location='query')
    def get(self, params: 'SearchQueryParam', ingredient_id):
        response, error = ingredients.get(ingredient_id, params)
        if error:
            return make_response(error, error['status_code'])
        return response, 200

    def put(self):
        pass

    def delete(self, id: int):
        response, err = ingredients.delete(id)
        if err:
            return err, err['status_code']
        return make_response(response, 204)
