from sqlalchemy import func

from app import db
from app.models.recipes import Recipe
from app.models.ingredients import Ingredient
from app.models.recipe_ingredients import RecipeIngredient


def get_ingredients_summary(recipe_ids: list):
    # ToDo: separar ingredientes opcionales
    # ToDo 1: agregar expiration times
    query = db.session.query(Ingredient, RecipeIngredient) \
            .join(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id) \
            .filter(RecipeIngredient.recipe_id.in_(recipe_ids)) \

    return query.with_entities(Ingredient.name, Ingredient.storage, RecipeIngredient.measure_unit, func.sum(RecipeIngredient.amount)).group_by(Ingredient.id, Ingredient.storage, RecipeIngredient.measure_unit).all()


def get_recipes_summary(recipe_ids: list):
    query = db.session.query(Recipe) \
        .filter(Recipe.id.in_(recipe_ids))

    return query.with_entities(func.sum(Recipe.cook_time), func.sum(Recipe.wash_time)).all()