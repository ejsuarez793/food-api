from flask import request
from flask_restx import Resource
from marshmallow import RAISE

from app.repositories import recipe_ingredients
from app.validators.recipes_search import VALID_FIELDS_FOR_SEARCH as VALID_FIELDS
from app.validators.ingredients_search import VALID_FIELDS_FOR_SEARCH as VALID_FIELDS_INGREDIENTS
from app.validators.searchs import SearchQuery, SearchQueryParser, SearchQueryParam

fields_query_parser = SearchQueryParser(valid_fields=VALID_FIELDS,
                                        valid_fields_ingredients=VALID_FIELDS_INGREDIENTS)


class RecipeByIdIngredient(Resource):

    @fields_query_parser.use_args(SearchQuery(unknown=RAISE), location='query')
    def get(self, params: 'SearchQueryParam', recipe_id: str):
        response, err = recipe_ingredients.get_recipe_with_ingredients(recipe_id, params)
        if err:
            return err, err['status_code']
        return response, 200

    def post(self, recipe_id: str):
        json_data = request.get_json()
        validate_empty_ingredients = True
        response, err = recipe_ingredients.add_ingredients_to_recipe(recipe_id, json_data, validate_empty_ingredients)
        if err:
            return err, err['status_code']
        return response, 201  # ToDo: revisar que status code sería correcto en este caso

    def put(self, recipe_id: str):
        json_data = request.get_json()
        validate_empty_ingredients = False
        response, err = recipe_ingredients.add_ingredients_to_recipe(recipe_id, json_data, validate_empty_ingredients)
        if err:
            return err, err['status_code']
        return response, 200

    def delete(self, recipe_id: str):
        response, err = recipe_ingredients.delete_recipe_ingredients(recipe_id)
        if err:
            return err, err['status_code']
        return response, 204
