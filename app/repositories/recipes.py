import uuid
import logging
import traceback
from app.recommendations_algoritms.recommendation_algorithm import RecommendationAlgorithm
from app.recommendations_algoritms.strategies.strategies import SimpleRecommendationStrategy

from app import db
from app.models.recipes import Recipe, RecipeSchema, RecipePaginationSchema
from app.dao import recipes_dao

log = logging.getLogger(__name__)

recommendation_algorithm = RecommendationAlgorithm(SimpleRecommendationStrategy())


def multiget(ids: list, fields: list):
    try:
        ingredients = Recipe.multiget(ids, fields)
    except Exception as e:
        log.error('there was a database error while getting ingredients [ids:%s][error:%s]', ','.join(ids), str(e))
        return None, {'msg': 'there was an error getting ingredients', 'status_code': 500}

    return RecipeSchema(many=True, only=fields).dump(ingredients), None


def search(params: 'SearchQueryParam'):

    if params.ids is not None:
        recipes, error = multiget(params.ids, params.fields)
        return recipes, error

    try:
        result = Recipe.search(params)
        res = {'paging': {'offset': params.offset, 'limit': params.limit},
               'results': result.items}
        # fields implementation to include only certain fields in response
        only = None
        if params.fields is not None:
            only = [f'results.{field}' for field in params.fields]
            only.append('paging')
        paginated_response = RecipePaginationSchema(only=only).dump(res)
        return paginated_response, None
    except Exception as e:
        log.error(f'there was a database error while searching recipes(s) [error:{str(e)}]')
        traceback.print_exc()
        return None, {'msg': 'there was an error searching recipes(s)', 'status_code': 500}


def get_by_id(id: str, params):
    return RecipeSchema().dump(Recipe.get_by_id(id, params.fields))


def create_recipe(data):
    recipe_schema = RecipeSchema()
    try:
        data['id'] = str(uuid.uuid4())
        validated_data = recipe_schema.load(data)
        new_recipe = Recipe(**validated_data)
    except Exception as e:
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
    return output


def delete_recipe(id):
    recipe = Recipe.query.filter(Recipe.id == id).first()
    if not recipe:
        return

    Recipe.query.filter(Recipe.id == id).delete()
    db.session.commit()


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
