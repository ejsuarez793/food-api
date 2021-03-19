"""
Routes file that maps Resources with endpoints
"""
from flask_restx import Api

from app.resources import (
    Recipe,
    RecipeById,
    Ingredient,
    IngredientById,
    RecipeRecommendation,
)

from app.resources.jobs.populate_db import PopulateDb


def register_routes(api: 'Api'):
    """
    Register api endpoints
    :param api: api object
    :return: Nothing
    """

    # recipes
    api.add_resource(Recipe, '/recipes', methods=['GET', 'POST'])
    api.add_resource(
        RecipeById, '/recipes/<string:id>', methods=['GET', 'PUT', 'DELETE']
    )
    api.add_resource(
        RecipeRecommendation, '/recipes/recommendations', methods=['GET']
    )

    # ingredients
    api.add_resource(Ingredient, '/ingredients', methods=['GET', 'POST'])
    api.add_resource(
        IngredientById,
        '/ingredients/<int:id>',
        methods=['GET', 'PUT', 'DELETE'],
    )

    # jobs
    api.add_resource(PopulateDb, '/jobs/populate_db', methods=['POST'])
