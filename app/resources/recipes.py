from flask import request, jsonify, make_response
from flask_restx import Resource
from marshmallow import RAISE

from app.repositories import recipes
from app.validators.recipes import RecipeSearchQueryParser
from app.validators.recipes import RecipeSearchQuery
from app.validators.recipes_recommendations import RecipesRecommendationsQueryParser, RecipesRecommendationsQueryParams

recipeSearchQueryParser = RecipeSearchQueryParser()

rrqp = RecipesRecommendationsQueryParser()


class Recipe(Resource):

    @recipeSearchQueryParser.use_args(RecipeSearchQuery(unknown=RAISE), location='query')
    def get(self, params: 'RecipeSearchQuery'):
        try:
            return recipes.get_with_params(params)
        except ValueError:
            return make_response(jsonify({'msg':'bad_request'}), 400)
        except:
            return make_response(jsonify({'msg':'internal_server_error'}), 500)

    def post(self):
        json_data = request.get_json()
        response, err = recipes.create_recipe(json_data)
        if err:
            return make_response(err, err['status_code'])
        return make_response(response, 201)


class RecipeById(Resource):

    def get(self, id: str):
        return recipes.get_by_id(id)

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
            return make_response(err, err['status_code']) # ToDo: remove make response
        return response
