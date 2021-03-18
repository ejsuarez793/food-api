"""
Ingredients repositories where all the services for
ingredients resources are located
"""

import uuid
import logging
from typing import Union, Dict

from marshmallow.exceptions import MarshmallowError
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.recipes import Recipe, RecipeSchema, RecipePaginationSchema

log = logging.getLogger(__name__)


def get_by_id(recipe_id: str) -> Dict:
    """
    Get recipe by id

    :param id: id uuid string
    :return: Recipe dict if found
    """

    return RecipeSchema().dump(Recipe.get_by_id(recipe_id))


def get_with_params(params: Dict) -> Dict:
    """
    Get recipes by pagination and date inteval from params
    :param params:
    :return:
    """

    # Todo: mejorar los try catch aquí, agregar SQLAlchemyException
    is_date_filtered_search = params.date_from is not None and \
                              params.date_to is not None
    if is_date_filtered_search:
        result = Recipe.get_by_pagination_and_date_range(params)
    else:
        result = Recipe.get_by_pagination(params)
    res = {'paging': {'offset': params.offset, 'limit': params.limit},
           'results': result.items}
    rps = RecipePaginationSchema()
    return rps.dump(res)


def create_recipe(data: Dict) -> Union[Dict, Dict]:
    """
    Create recipe from data dict param

    :param data: dict with information of recipe to be created
    :return: dict with newly created recipe
    """

    recipe_schema = RecipeSchema()
    try:
        data['id'] = str(uuid.uuid4())
        validated_data = recipe_schema.load(data)
        new_recipe = Recipe(**validated_data)
    except MarshmallowError:
        log.exception('there was an error validating recipe: [data:%s]', str(data))
        return None, {'msg': 'there was an error validating recipe', 'status_code': 400}

    try:
        db.session.add(new_recipe)
        db.session.commit()
    except SQLAlchemyError:
        log.exception('there was an error creating recipe: [data:%s]', str(data))
        return None, {'msg': 'there was an error creating recipe', 'status_code': 500}

    return recipe_schema.dump(new_recipe), None


def update_recipe(recipe_id: str, data: Dict) -> Union[Dict, Dict]:
    """
    Update recipe by id (uuid string) and new fields in data to be updated

    :param id: uuid string that represents recipe id
    :param data: dict with all the recipe data to be updated
    :return: updated recipe dict
    """

    # ToDo: agregar try except aquí
    recipe = Recipe.get_by_id(recipe_id)

    recipe.name = data['name']

    db.session.add(recipe)
    db.session.commit()

    recipe_schema = RecipeSchema()
    output = recipe_schema.dump(recipe)
    return output


def delete_recipe(recipe_id: str):
    """
    Delete recipe by id
    :param id: id uuid string
    :return:
    """

    # ToDo: agregar try except aqui
    recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
    if not recipe:
        return

    Recipe.query.filter(Recipe.id == recipe_id).delete()
    db.session.commit()
