import logging

from marshmallow import ValidationError

from app import db
from app.models.ingredients import IngredientSchema, Ingredient

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
        validated_ids = [int(id) for id in ids]
    except Exception as e:
        log.debug('invalid params for ingredients multiget [ids:%s]',','.join(ids))
        return None, {'msg': 'invalid params for multiget', 'status_code': 400}

    try:
        ingredients = Ingredient.multiget(validated_ids)
    except Exception as e:
        log.error('there was a database error while getting ingredients [ids:%s][error:%s]', ','.join(validated_ids), str(e))
        return None, {'msg': 'there was an error getting ingredients', 'status_code': 500}

    return IngredientSchema(many=True).dump(ingredients), None


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
