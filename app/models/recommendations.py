from app import ma
from app import db

from marshmallow import fields

from app.models.recipes import RecipeSchema
from app.models.recipe_ingredients import RecipeIngredientResponseSchema
from app.models.recipes import Recipe


class Recommendation:

    @staticmethod
    def get_recipes():
        query = Recipe.query.unnest()


class RecommendationSchema(ma.Schema):
    meal_types = fields.Nested(fields.String())
    days = fields.Integer()
    veggie_friendly = fields.Boolean()
    ingredients = fields.Nested(RecipeIngredientResponseSchema(), many=True)
    recommendations = fields.Nested(RecipeSchema(), many=True)