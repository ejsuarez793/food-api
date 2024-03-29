import uuid
import logging
import traceback

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from marshmallow.exceptions import ValidationError

from app.recommendations_algoritms.recommendation_algorithm import RecommendationAlgorithm
from app.recommendations_algoritms.strategies.strategies import SimpleRecommendationStrategy

from app import db
from app.models.recipes import Recipe, RecipeSchema, RecipePaginationSchema
from app.dao import recipes_dao

log = logging.getLogger(__name__)

recommendation_algorithm = RecommendationAlgorithm(SimpleRecommendationStrategy())


"""
    RECIPES METHODS
"""


def multiget(ids: list, fields: list):
    try:
        ingredients = Recipe.multiget(ids, fields)
    except Exception as e:
        log.error('there was a database error while performing multiget on recipes [ids:%s][error:%s]', ','.join(ids), str(e))
        return None, {'msg': 'there was an error getting ingredients', 'status_code': 500}

    return RecipeSchema(many=True).dump(ingredients), None


def search(params: 'SearchQueryParam'):
    # ToDo: la respuesta del search cambia dependiendo de los parámetros (lista vs paginación) revisar si mover esto (?)
    if params.ids is not None:
        recipes, error = multiget(params.ids, params.fields)
        return jsonify(recipes), error  # note that this jsonify is necessary

    try:
        result = Recipe.search(params)
        res = {'paging': {'offset': params.offset, 'limit': params.limit},
               'results': result.items}
        paginated_response = RecipePaginationSchema().dump(res)
        return paginated_response, None
    except SQLAlchemyError as e:
        log.error(f'there was a database error while searching recipes(s) [error:{str(e)}]')
        traceback.print_exc()
        return None, {'msg': 'there was an error searching recipes(s)', 'status_code': 500}


def create_recipe(data):

    try:
        recipe_schema = RecipeSchema()
        data['id'] = str(uuid.uuid4())
        validated_data = recipe_schema.load(data)
        new_recipe = Recipe(**validated_data)

        db.session.add(new_recipe)
        db.session.commit()
        return recipe_schema.dump(new_recipe), None
    except ValidationError:
        log.debug('invalid recipe data') # ToDo: reenviar msg asignados en la validación
        traceback.print_exc()
        return None, {'msg': 'there was an error validating recipe', 'status_code': 400}
    except SQLAlchemyError:
        log.error('there was a databaser error while creating recipe')
        traceback.print_exc()
        return None, {'msg': 'there was an error creating recipe', 'status_code': 500}


"""
    RECIPE BY ID METHODS
"""


def get_recipe_by_id(recipe_id: str, params: 'SearchQueryParam'):

    try:
        recipe = Recipe.get_by_id(recipe_id, params.fields)
        return RecipeSchema().dump(recipe), None
    except SQLAlchemyError:
        log.error(f'there was a database error while getting recipe by id [recipe_id:{recipe_id}]')
        traceback.print_exc()
        return None, {'msg': 'there was an error getting recipe', 'status_code': 500}


def update_recipe(recipe_id: str, data: dict):

    try:
        recipe_schema = RecipeSchema()
        validated_data = recipe_schema.load(data, partial=True)
        recipe = Recipe.get_by_id(recipe_id)
        for attribute in validated_data:
            setattr(recipe, attribute, validated_data[attribute])
        db.session.add(recipe)
        db.session.commit()
        return recipe_schema.dump(recipe), None
    except ValidationError:
        log.error(f'there was an error while parsing data for recipe update [id:{recipe_id}]')
        traceback.print_exc()
        return None, {'msg': 'invalid data for recipe', 'status_code': 400}
    except SQLAlchemyError:
        log.error(f'there was a database error while updating recipe [id:{recipe_id}]')
        traceback.print_exc()
        return None, {'msg': 'there was an error while updating recipe', 'status_code': 500}


def delete_recipe(recipe_id: str):

    try:
        recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
        if recipe:
            Recipe.query.filter(Recipe.id == recipe_id).delete()
            db.session.commit()
    except SQLAlchemyError:
        log.error(f'there was a database error while deleting recipe [id:{recipe_id}]')
        traceback.print_exc()
        return None, {'msg': 'there was an error deleting ingredient', 'status_code': 500}

    return {}, None


"""
    RECOMMENDATIONS METHODS
"""


def get_recommendations(params):
    try:
        recipes = recipes_dao.get_recommendations(params.veggie_only, params.meals)
    except Exception as e:
        log.error('there was an error getting recommendations from recipe dao [error:{}]'.format(str(e)))
        return None, {'msg': 'there was an error getting recommendations', 'status_code': 500}

    try:
        response = recommendation_algorithm.do_recommendation(recipes, params)
    except Exception as e:
        log.error('there was an error preparing recommendation [error:{}]'.format(str(e)))
        return None, {'msg': 'there was an error getting recommendations', 'status_code': 500}

    return response, None
