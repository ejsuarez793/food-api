from flask_restx import Api

from app.resources import Recipe, \
    RecipeById, \
    Ingredient, \
    IngredientById, \
    RecipeByIdIngredient, \
    RecipeByIdIngredientById, \
    Recommendation, \
    Summary

from app.resources.jobs.populate_db import PopulateDb


def register_routes(api: 'Api'):
    # recipes
    api.add_resource(Recipe, '/recipes', methods=['GET', 'POST'])
    api.add_resource(RecipeById, '/recipes/<string:recipe_id>', methods=['GET', 'PUT', 'DELETE'])

    # ingredients
    api.add_resource(Ingredient, '/ingredients', methods=['GET', 'POST'])
    api.add_resource(IngredientById, '/ingredients/<int:ingredient_id>', methods=['GET', 'PUT', 'DELETE'])

    # recipes ingredients
    api.add_resource(RecipeByIdIngredient, '/recipes/<string:recipe_id>/ingredients', methods=['GET', 'POST', 'PUT', 'DELETE'])
    api.add_resource(RecipeByIdIngredientById, '/recipes/<string:recipe_id>/ingredients/<int:ingredient_id>', methods=['DELETE'])

    # recommendations
    api.add_resource(Recommendation, '/recommendations', methods=['GET'])

    api.add_resource(Summary, '/summaries', methods=['POST'])

    # jobs
    api.add_resource(PopulateDb, '/jobs/populate_db', methods=['POST'])
