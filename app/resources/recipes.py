from flask import request, make_response
from flask_restx import Resource
from marshmallow import RAISE
from flasgger import swag_from

from app.swagger.recipes import spec_dict
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

    @swag_from(spec_dict['recipe']['get'])
    @search_query_parser.use_args(SearchQuery(unknown=RAISE), location='query')
    def get(self, params: 'SearchQueryParam'):
        response, error = recipes.search(params)
        if error:
            return make_response(error, error['status_code'])
        return make_response(response, 200)

    @swag_from(spec_dict['recipe']['post'])
    def post(self):
        json_data = request.get_json()
        response, err = recipes.create_recipe(json_data)
        if err:
            return make_response(err, err['status_code'])
        return make_response(response, 201)


class RecipeById(Resource):

    @swag_from(spec_dict['recipe_by_id']['get'])
    @fields_query_parser.use_args(SearchQuery(unknown=RAISE), location='query')
    def get(self,  params: 'SearchQueryParam', recipe_id: str):
        response, error = recipes.get_recipe_by_id(recipe_id, params)
        if error:
            make_response(error, error['status_code'])
        return make_response(response, 200)

    @swag_from(spec_dict['recipe_by_id']['put'])
    def put(self, recipe_id: str):
        json_data = request.get_json()
        response, err = recipes.update_recipe(recipe_id, json_data)
        if err:
            return make_response(err, err['status_code'])
        return make_response(response, 200)

    @swag_from(spec_dict['recipe_by_id']['delete'])
    def delete(self, recipe_id: str):
        response, error = recipes.delete_recipe(recipe_id)
        if error:
            make_response(error, error['status_code'])
        return make_response(response, 204)


class RecipeRecommendation(Resource):

    @rrqp.use_args(RecipesRecommendationsQueryParams(unknown=RAISE), location='query')
    def get(self, params: 'RecipesRecommendationsQueryParams'):
        response, err = recipes.get_recommendations(params)
        if err:
            return make_response(err, err['status_code'])  # ToDo: remove make response
        return make_response(response, 200)
