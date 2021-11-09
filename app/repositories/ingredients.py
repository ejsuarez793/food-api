import logging
import traceback

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from app import db
from app.models.ingredients import IngredientSchema, Ingredient, IngredientPaginationSchema

log = logging.getLogger(__name__)

"""
    INGREDIENT METHODS
"""


def multiget(ids: list, fields: list):
    try:
        ingredients = Ingredient.multiget(ids, fields)
    except SQLAlchemyError as e:
        log.error('there was a database error while getting ingredients [ids:%s][error:%s]', ','.join(ids), str(e))
        return None, {'msg': 'there was an error getting ingredients', 'status_code': 500}

    return IngredientSchema(many=True).dump(ingredients), None


def search(params: 'SearchQueryParam'):

    # ToDo: la respuesta del search cambia dependiendo de los parámetros (lista vs paginación) revisar si mover esto (?)
    if params.ids is not None:
        ingredients, error = multiget(params.ids, params.fields)
        return jsonify(ingredients), error # Note this jsonify is necessary

    try:
        result = Ingredient.search(params)
        res = {'paging': {'offset': params.offset, 'limit': params.limit},
               'results': result.items}
        paginated_response = IngredientPaginationSchema().dump(res)  # Todo Instaciar siempre pagination Schema
        return paginated_response, None
    except Exception as e:
        log.error(f'there was a database error while searching ingredient(s) [error:{str(e)}]')
        traceback.print_exc()  # ToDo agregar esto en lugares importantes, o en todos los try catch mejor (?)
        return None, {'msg': 'there was an error searching ingredient(s)', 'status_code': 500}


def create_ingredient(data: dict):

    try:
        schema = IngredientSchema()
        validated_data = schema.load(data)
        new_ingredient = Ingredient(**validated_data)

        db.session.add(new_ingredient)
        db.session.commit()

        return schema.dump(new_ingredient), None
    except ValidationError:
        log.debug('there was an error validating ingredient')
        traceback.print_exc()
        return None, {'msg': 'there was an error validating ingredient', 'status_code': 400}
    except SQLAlchemyError:
        log.error('there was a database error creating ingredient')
        traceback.print_exc()
        return None, {'msg': 'there was an error creating ingredient', 'status_code': 500}


"""
    INGREDIENT BY ID METHODS
"""


def get_ingredient_by_id(id: int, params: 'IngredientQuery'):
    try:
        ingredient = Ingredient.get_by_id(id, params.fields)
    except SQLAlchemyError as e:
        log.error('there was a database error while getting ingredient [id:{}][error:{}]'.format(id, str(e)))
        return None, {'msg': 'there was and error while looking for ingredient', 'status_code': 500}
    return IngredientSchema().dump(ingredient), None


def update_ingredient(id: int, data: dict):

    try:
        ingredient_schema = IngredientSchema()
        validated_data = ingredient_schema.load(data, partial=True)
        ingredient = Ingredient.get_by_id(id)
        for attribute in validated_data:
            setattr(ingredient, attribute, validated_data[attribute])
        db.session.add(ingredient)
        db.session.commit()
        return ingredient_schema.dump(ingredient), None
    except ValidationError:
        # ToDo: retornar msg error en la validación en vez de simplemente invalid data
        log.error(f'there was an error while parsing data for ingredient update [id:{id}]')
        traceback.print_exc()
        return None, {'msg': 'invalid data for ingredient', 'status_code': 400}
    except SQLAlchemyError:
        log.error(f'there was a database error while updating ingredient [id:{id}]')
        traceback.print_exc()
        return None, {'msg': 'there was an error while updating ingredient', 'status_code': 500}


def delete_ingredient(id: int):

    try:
        ingredient = Ingredient.query.filter(Ingredient.id == id).first()
        if ingredient:
            Ingredient.query.filter(Ingredient.id == id).delete()
            db.session.commit()
    except SQLAlchemyError:
        log.error(f'there was a database error deleting ingredient [id:{id}]')
        traceback.print_exc()
        return None, {'msg': 'there was an error deleting ingredient', 'status_code': 500}

    return {}, None
