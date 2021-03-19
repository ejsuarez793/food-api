"""
Resources for recipes, basically like Resources controllers
that communicates with repositories as needed

Defines three recipe resource: Recipe, RecipeById and RecipeRecommendation
just because method get needs to have different logic based on route
and params
"""

from flask import request, jsonify, make_response
from flask_restx import Resource
from marshmallow import RAISE

from app.repositories import recipes
from app.validators.recipes import RecipeSearchQueryParser
from app.validators.recipes import RecipeSearchQuery
from app.validators.recipes_recommendations import (
    RecipesRecommendationsQueryParser,
    RecipesRecommendationsQueryParams,
)

recipeSearchQueryParser = RecipeSearchQueryParser()

rrqp = RecipesRecommendationsQueryParser()


class Recipe(Resource):
    """
    Recipe Resource for general CRUD methods
    """

    @recipeSearchQueryParser.use_args(
        RecipeSearchQuery(unknown=RAISE), location='query'
    )
    def get(self, params: 'RecipeSearchQuery'):
        """
        Get recipes based of query params

        :param params: RecipeSearchQuery object parsed from query params
        :return: recipes result on succes, bad request or internal server
        error otherwise
        """

        try:
            return recipes.get_with_params(params)
        except ValueError:
            return make_response(jsonify({'msg': 'bad_request'}), 400)
        except:
            return make_response(
                jsonify({'msg': 'internal_server_error'}), 500
            )

    def post(self):
        """
        post method to create recipes
        :return: newly created recipe on success, error otherwise
        """

        json_data = request.get_json()
        response, err = recipes.create_recipe(json_data)
        if err:
            return make_response(err, err['status_code'])
        return make_response(response, 201)


class RecipeById(Resource):
    """
    RecipeById for id-based methods
    """

    def get(self, recipe_id: str):
        """
        Get recipe by id
        :param recipe_id: recipe id uuid str
        :return: recipe if found
        """

        return recipes.get_by_id(recipe_id)

    def put(self, recipe_id: str):
        """
        Put recipe by id
        :param recipe_id: recipe_id uuid str
        :return: updated recipe
        """

        json_data = request.get_json()
        return recipes.update_recipe(recipe_id, json_data)

    def delete(self, recipe_id: str):
        """
        Delete recipe by id
        :param recipe_id: recipe_id uuid str
        :return: 204 always
        """

        return recipes.delete_recipe(recipe_id), 204


class RecipeRecommendation(Resource):
    """
    RecipeRecommendation for recommendations methods
    """

    @rrqp.use_args(
        RecipesRecommendationsQueryParams(unknown=RAISE), location='query'
    )
    def get(self, params: 'RecipesRecommendationsQueryParams'):
        """
        get method
        :param params: params
        :return: retu
        """

        print(type(params))
        print(params)
        pass
