import logging
import traceback
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

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
    except SQLAlchemyError:
        log.error(f'there was a database error while looking recipe with ingredients [recipe:{recipe_id}]')
        traceback.print_exc()
        return None, {'msg': 'there was and error while looking for recipe ingredients', 'status_code': 500}

    if recipe is None:
        return None, {'msg': f'recipe with \'id\' {recipe_id} does not exits', 'status_code': 404}

    try:
        ingredients = RecipeIngredient.get_ingredients(recipe_id)
    except SQLAlchemyError:
        log.error(f'there was a database error while looking ingredients for recipe with ingredients [recipe:{recipe_id}]')
        traceback.print_exc()
        return None, {'msg': 'there was and error while looking for recipe ingredients', 'status_code': 500}

    response = RecipeSchema().dump(recipe)
    response['ingredients'] = IngredientSchema(many=True).dump(ingredients)

    return response, None


def add_ingredients_to_recipe(recipe_id, json_data, validate_empty_ingredients):
    recipe_ingredient_schema = RecipeIngredientSchema(many=True)

    # check if recipe already has ingredients associated
    try:
        if validate_empty_ingredients:
            ingredients_number = RecipeIngredient.get_ingredients_number(recipe_id)
            if ingredients_number != 0:
                return None, {'msg': f'recipe \'{recipe_id}\' already have ingredients associated, '
                                 f'please use PUT request to add additional ingredients', 'status_code': 400}
    except SQLAlchemyError:
        log.error('there was a database error counting number of ingredients for recipe: [{error}]'.format(error=str(e)))
        traceback.print_exc()
        return None, {'msg': 'there was an error adding ingredients to recipe', 'status_code': 500}

    # validate recipe_id
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

    # bulk save into db
    try:
        db.session.bulk_save_objects(new_recipe_ingredients)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()  # ToDo: agregar rollback en otros casos (?)
        traceback.print_exc()
        return None, {'msg': 'a ingredient already exists for recipe', 'status_code': 500}
    except SQLAlchemyError as e:
        log.error(f'there was a database error while bulk saving ingredients to recipe: [error:{str(e)}]')
        return None, {'msg': 'there was an error adding ingredients to recipe', 'status_code': 500}

    return recipe_ingredient_schema.dump(new_recipe_ingredients), None


def delete_recipe_ingredients(recipe_id: str):

    try:
        RecipeIngredient.delete_all_ingredients(recipe_id)
        db.session.commit()
    except SQLAlchemyError as e:
        log.error(f'there was a database error while deleting recipe {recipe_id} ingredients')
        traceback.print_exc()
        db.session.rollback()
        return None, {'msg': f'there was a database error while deleting ingredients for recipe {recipe_id}', 'status_code': 500}
    return "", None
