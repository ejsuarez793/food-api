"""
Ingredients repositories where all the services for ingredients resources are located
"""

import logging
from typing import Union, List, Dict

from marshmallow import ValidationError

from app import db
from app.models.ingredients import IngredientSchema, Ingredient

log = logging.getLogger(__name__)


def get(ingredient_id: int) -> Union[Dict, Dict]:
    """
    Get ingredient by id

    :param ingredient_id: int
    :return: Ingredient object if found, None and an error if otherwhise
    """

    try:
        ingredient = Ingredient.get_by_id(ingredient_id)
    except Exception as exception:
        log.error('there was a database error while getting ingredient [id:{}][error:{}]'
                  .format(ingredient_id, str(exception)))
        return None, {'msg': 'there was and error while looking for ingredient', 'status_code': 500}

    return IngredientSchema().dump(ingredient), None


def multiget(ids: List[int]) -> Union[List[Dict], Dict]:
    """
    Executes a multiget search given a list of ids

    :param ids: List of ints representing the ids to lookup
    :return: List of Dict with the ingredients found if an error occurs
    then returns None with an error msg
    """

    try:
        validated_ids = [int(id) for id in ids]
    except Exception:
        log.debug('invalid params for ingredients multiget [ids:%s]',','.join(ids))
        return None, {'msg': 'invalid params for multiget', 'status_code': 400}

    try:
        ingredients = Ingredient.multiget(validated_ids)
    except Exception as exception:
        log.error('there was a database error while getting ingredients [ids:%s][error:%s]',
                  ','.join(validated_ids), str(exception))
        return None, {'msg': 'there was an error getting ingredients', 'status_code': 500}

    return IngredientSchema(many=True).dump(ingredients), None


def create(data: Dict) -> Union[Dict, Dict]:
    """
    Creates an ingredient from data dict and returns the newly created ingredient
    and None error dict otherwise returns None object an a dict with error msg and
    error status code

    :param data: dict with ingredient data
    :return: dict with ingredient data or error dict
    """

    schema = IngredientSchema()
    try:
        validated_data = schema.load(data)
        new_ingredient = Ingredient(**validated_data)
    except ValidationError as exception:
        log.debug('there was an error validating ingredient: [{error}]'.format(error=str(exception)))
        return None, {'msg': 'there was an error validating ingredient', 'status_code': 400}

    try:
        db.session.add(new_ingredient)
        db.session.commit()
    except Exception as exception:
        log.error('there was a database error creating ingredient [error:{}]'.format(str(exception)))
        return None, {'msg': 'there was an error creating ingredient', 'status_code': 500}

    return schema.dump(new_ingredient), None


def delete(id: int) -> Union[Dict, Dict]:
    """
    Deletes ingredient by id

    :param id: Id of the ingredient to delete
    :return: empty union of two dicts on success, otherwise a dict with error msg
    """

    # Todo: este validacion del .first() hace falta? o solo el .delete() ya esta
    try:
        recipe = Ingredient.query.filter(Ingredient.id == id).first()
    except Exception as exception:
        log.error('there was a database error finding ingredient for deletion [id:%d][error:%s]',id, str(exception))
        return None, {'msg': 'there was an error deleting ingredient', 'status_code': 500}

    if not recipe:
        return {}, None

    try:
        Ingredient.query.filter(Ingredient.id == id).delete()
        db.session.commit()
    except Exception as exception:
        log.error('there was a database error deleting ingredient [id:%d][error:%s]', id, str(exception))
        return None, {'msg': 'there was an error deleting ingredient', 'status_code': 500}

    return {}, None
