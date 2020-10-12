from flask_restx import Api

from app.resources import Recipe, RecipeById, Ingredient, IngredientById

def register_routes(api: 'Api'):
    # recipes
    api.add_resource(Recipe, '/recipes', methods=['GET','POST'])
    api.add_resource(RecipeById, '/recipes/<string:id>', methods=['GET', 'PUT', 'DELETE'])

    # ingredients
    api.add_resource(Ingredient, '/ingredients', methods=['GET', 'POST'])
    api.add_resource(IngredientById, '/ingredients/<int:id>', methods=['GET', 'PUT', 'DELETE'])