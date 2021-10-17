from flask import request, make_response
from flask_restx import Resource
from marshmallow import RAISE

from app.repositories import recipes
from app.validators.recipes_recommendations import RecipesRecommendationsQueryParser, RecipesRecommendationsQueryParams
from app.validators.searchs import SearchQuery, SearchQueryParser, SearchQueryParam

from app.validators.recipes_search import VALID_FIELDS_FOR_SEARCH, \
    VALID_FILTERS, FILTERS_DATA_TYPES, STR_COLUMNS, NUMERIC_COLUMNS

rrqp = RecipesRecommendationsQueryParser()

search_query_parser = SearchQueryParser(valid_filters=VALID_FILTERS,
                                        filters_data_types=FILTERS_DATA_TYPES,
                                        str_columns=STR_COLUMNS,
                                        numeric_columns=NUMERIC_COLUMNS,
                                        valid_fields=VALID_FIELDS_FOR_SEARCH,
                                        int_ids=False)

fields_query_parser = SearchQueryParser(valid_fields=VALID_FIELDS_FOR_SEARCH)


class Recipe(Resource):

    @search_query_parser.use_args(SearchQuery(unknown=RAISE), location='query')
    def get(self, params: 'SearchQueryParam'):
        response, error = recipes.search(params)
        if error:
            return error, error['status_code']
        return response, 200

    def post(self):
        json_data = request.get_json()
        response, err = recipes.create_recipe(json_data)
        if err:
            return make_response(err, err['status_code'])
        return make_response(response, 201)


class RecipeById(Resource):

    @fields_query_parser.use_args(SearchQuery(unknown=RAISE), location='query')
    def get(self,  params: 'FieldsQueryParam', id: str):
        print(params)
        return recipes.get_by_id(id, params)

    def put(self, id: str):
        json_data = request.get_json()
        return recipes.update_recipe(id, json_data)

    def delete(self, id: str):
        return recipes.delete_recipe(id), 204


class RecipeRecommendation(Resource):

    @rrqp.use_args(RecipesRecommendationsQueryParams(unknown=RAISE), location='query')
    def get(self, params: 'RecipesRecommendationsQueryParams'):
        response, err = recipes.get_recommendations(params)
        if err:
            return make_response(err, err['status_code'])  # ToDo: remove make response
        return response
