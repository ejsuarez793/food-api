import logging
import traceback
import json

from app import db

from app.models.recipes import Recipe, RecipeSchema
from app.models.ingredients import IngredientSchema
from app.models.recipe_ingredients import RecipeIngredient, RecipeIngredientSchema

log = logging.getLogger(__name__)


def get_recipe_with_ingredients(recipe_id):
    #ToDo: mejorar try catch, revisar como validar que exista la recipe y ver que pasa si no tiene ingredientes
    # ToDo (cont): si no tiene ingredientes no pasa nada :D
    try:
        recipe = Recipe.get_by_id(recipe_id)
    except Exception as e:
        log.error(f'there was a database error while looking recipe with ingredients [recipe:{recipe_id}]')
        traceback.print_exc()
        return None, {'msg': 'there was and error while looking for recipe ingredients', 'status_code': 500}

    if recipe is None:
        return None, {'msg': f'recipe with \'id\' {recipe_id} does not exits', 'status_code': 404}

    try:
        ingredients = RecipeIngredient.get_ingredients(recipe_id)
    except Exception as e:
        log.error(f'there was a database error while looking ingredients for recipe with ingredients [recipe:{recipe_id}]')
        traceback.print_exc()
        return None, {'msg': 'there was and error while looking for recipe ingredients', 'status_code': 500}

    response = RecipeSchema().dump(recipe)
    response['ingredients'] = IngredientSchema(many=True).dump(ingredients)

    return response, Nonegi


def add_ingredients_to_recipe(recipe_id, json_data):
    recipe_ingredient_schema = RecipeIngredientSchema(many=True)
    try:
        for data in json_data:
            data['recipe_id'] = recipe_id
        validated_data = recipe_ingredient_schema.load(json_data)

        new_recipe_ingredients = []
        for valid_data in validated_data:
            new_recipe_ingredients.append(RecipeIngredient(**valid_data))
    except Exception as e:
        log.debug('there was an error validating recipe ingredients: [{error}]'.format(error=str(e)))
        traceback.print_exc()
        return None, {'msg': 'there was an error validating recipe ingredients', 'status_code': 400}

    try:
        db.session.bulk_save_objects(new_recipe_ingredients)
        db.session.commit()
    except Exception as e:
        log.error('there was an error adding ingredients to recipe: [{error}]'.format(error=str(e)))
        return None, {'msg': 'there was an error adding ingredients to recipe', 'status_code': 500}

    return recipe_ingredient_schema.dump(new_recipe_ingredients), None

