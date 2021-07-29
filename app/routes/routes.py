from flask_restx import Api

from app.resources import Recipe, RecipeById, Ingredient, IngredientById, RecipeRecommendation, RecipeIngredientById

from app.resources.jobs.populate_db import PopulateDb

def register_routes(api: 'Api'):
    # recipes
    api.add_resource(Recipe, '/recipes', methods=['GET', 'POST'])
    api.add_resource(RecipeById, '/recipes/<string:id>', methods=['GET', 'PUT', 'DELETE'])
    api.add_resource(RecipeIngredientById, '/recipes/<string:recipe_id>/ingredients', methods=['GET', 'POST', 'PUT', 'DELETE'])
    api.add_resource(RecipeRecommendation, '/recipes/recommendations', methods=['GET'])

    # ingredients
    api.add_resource(Ingredient, '/ingredients', methods=['GET', 'POST'])
    api.add_resource(IngredientById, '/ingredients/<int:id>', methods=['GET', 'PUT', 'DELETE'])

    # jobs
    api.add_resource(PopulateDb, '/jobs/populate_db', methods=['POST'])