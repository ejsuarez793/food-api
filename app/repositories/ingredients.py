import logging
import traceback

from marshmallow import ValidationError

from app import db
from app.models.ingredients import IngredientSchema, Ingredient, IngredientPaginationSchema

log = logging.getLogger(__name__)


def get(id: int):
    try:
        ingredient = Ingredient.get_by_id(id)
    except Exception as e:
        log.error('there was a database error while getting ingredient [id:{}][error:{}]'.format(id, str(e)))
        return None, {'msg': 'there was and error while looking for ingredient', 'status_code': 500}

    return IngredientSchema().dump(ingredient), None


def multiget(ids: list):
    try:
        ingredients = Ingredient.multiget(ids)
    except Exception as e:
        log.error('there was a database error while getting ingredients [ids:%s][error:%s]', ','.join(ids), str(e))
        return None, {'msg': 'there was an error getting ingredients', 'status_code': 500}

    return IngredientSchema(many=True).dump(ingredients), None


def search(params: 'IngredientSearchQuery'):

    if params.ids is not None:
        return multiget(params.ids)

    try:
        result = Ingredient.search(params)
        res = {'paging': {'offset': params.offset, 'limit': params.limit},
               'results': result.items}
        ips = IngredientPaginationSchema()
        return ips.dump(res), None
    except Exception as e:
        log.error(f'there was a database error while searching ingredient(s) [error:{str(e)}]')
        traceback.print_exc()  # ToDo agregar esto en lugares importantes, o en todos los try catch mejor (?)
        return None, {'msg': 'there was an error searching ingredient(s)', 'status_code': 500}

def create(data):
    schema = IngredientSchema()
    try:
        validated_data = schema.load(data)
        new_ingredient = Ingredient(**validated_data)
    except ValidationError as e:
        log.debug('there was an error validating ingredient: [{error}]'.format(error=str(e)))
        return None, {'msg': 'there was an error validating ingredient', 'status_code': 400}

    try:
        db.session.add(new_ingredient)
        db.session.commit()
    except Exception as e:
        log.debug('there was a database error creating ingredient', str(e))
        return None, {'msg': 'there was an error creating ingredient', 'status_code': 500}

    return schema.dump(new_ingredient), None


def delete(id: int):
    # Todo: este validacion del .first() hace falta? o solo el .delete() ya esta
    try:
        recipe = Ingredient.query.filter(Ingredient.id == id).first()
    except Exception as e:
        log.error('there was a database error finding ingredient for deletion [id:%d]', id)
        return None, {'msg': 'there was an error deleting ingredient', 'status_code': 500}

    if not recipe:
        return {}, None

    try:
        Ingredient.query.filter(Ingredient.id == id).delete()
        db.session.commit()
    except Exception as e:
        log.error('there was a database error deleting ingredient [id:%d]', id)
        return None, {'msg': 'there was an error deleting ingredient', 'status_code': 500}

    return {}, None
