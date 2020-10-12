import uuid
import logging
from marshmallow import ValidationError

from app import db
from app.models.recipes import Recipe, RecipeSchema, RecipePaginationSchema

log = logging.getLogger(__name__)

def get_by_id(id: str):
    return RecipeSchema().dump(Recipe.get_by_id(id))


def get_with_params(params: dict):

    isDateFilteredSearch = params.date_from is not None and params.date_to is not None
    if isDateFilteredSearch:
        result = Recipe.get_by_pagination_and_date_range(params)
    else:
        result = Recipe.get_by_pagination(params)

    res = {'paging': {'offset': params.offset, 'limit': params.limit},
           'results': result.items}
    rps = RecipePaginationSchema()
    return rps.dump(res)


def create_recipe(data):
    recipe_schema = RecipeSchema()
    try:
        data['id'] = str(uuid.uuid4())
        validated_data = recipe_schema.load(data)
        new_recipe = Recipe(**validated_data)
    except ValidationError as e:
        log.debug('there was an error validating recipe: [{error}]'.format(error=str(e)))
        return None, {'msg': 'there was an error validating recipe', 'status_code': 400}

    try:
        db.session.add(new_recipe)
        db.session.commit()
    except Exception as e:
        log.error('there was an error creating recipe: [{error}]'.format(error=str(e)))
        return None, {'msg': 'there was an error creating recipe', 'status_code': 500}

    return recipe_schema.dump(new_recipe), None


def update_recipe(id, data):
    recipe = Recipe.get_by_id(id)

    recipe.name = data['name']

    db.session.add(recipe)
    db.session.commit()

    recipe_schema = RecipeSchema()
    output = recipe_schema.dump(recipe)
    return jsonify(output)


def delete_recipe(id):
    recipe = Recipe.query.filter(Recipe.id == id).first()
    if not recipe:
        return

    Recipe.query.filter(Recipe.id == id).delete()
    db.session.commit()