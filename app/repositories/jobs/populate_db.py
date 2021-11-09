import csv
import logging
import requests as r
import traceback

import dataclasses
from typing import List

API_ENDPOINT_RECIPES = 'http://localhost:5000/recipes'
API_ENDPOINT_INGREDIENTS = 'http://localhost:5000/ingredients'
API_ENDPOINT_RECIPES_INGREDIENTS = 'http://localhost:5000/recipes/{recipe_id}/ingredients/'
log = logging.getLogger(__name__)


@dataclasses.dataclass
class Recipe:
    name: str
    veggie_friendly: bool
    meal_type: str
    cook_time: int
    wash_time: int
    cook_technique: str
    ingredients: List[str]
    ingredients_ids: List[str]
    info: str
    steps: str


def __read_recipes_csv():
    recipes = []

    try:
        with open('recipes_to_load.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                recipe = dict()
                recipe['name'] = row['name']
                recipe['veggie_friendly'] = row['veggie_friendly']
                recipe['veggie_friendly'] = bool(row['veggie_friendly'])
                recipe['meal_type'] = row['meal_type'].split('/')
                recipe['cook_time'] = int(row['cook_time'])
                recipe['wash_time'] = int(row['wash_time'])
                recipe['cook_technique'] = row['cook_technique']
                recipe['info'] = row['info']
                recipe['steps'] = row['steps']

                try:
                    ingredients = []
                    for ingredient_quantity_and_meassure_unit in row['ingredients'].split('|'):
                        splitted = ingredient_quantity_and_meassure_unit.split(';')
                        ingredient_name = splitted[0]
                        amount = splitted[1]
                        measure_unit = splitted[2]
                        optional = True if splitted[3] == 'opcional' else None

                        ingredients.append({'ingredient_name': ingredient_name,
                                            'amount': amount,
                                            'measure_unit': measure_unit,
                                            'optional': optional})
                except Exception as e:
                    log.error(f'there was an error parsing recipe {recipe["name"]} ingredients')
                    raise r

                recipe['ingredients'] = ingredients
                recipe['ingredients_ids'] = []
                reci = Recipe(**recipe)

                recipes.append(reci)
    except Exception as e:
        error_msg = 'there was an error reading recipes to load file [error:{}]'.format(str(e))
        log.error(error_msg)
        raise e

    return recipes


def __get_ingredient_id_by_name(ingredient_name: str) -> str:
    headers = {'content-type': 'application/json'}
    query_param_filter = f'name[eq]={ingredient_name}'
    url = r.utils.requote_uri(f'{API_ENDPOINT_INGREDIENTS}?{query_param_filter}')
    # log.debug(f'Making request to endpoint url [{url}]')
    try:
        res = r.get(url=url, headers=headers)
        if res.status_code == 200:
            results = res.json()['results']
            if len(results) == 0:
                log.info(f'ingredient {ingredient_name} has no results')
                return None, True
            return results[0]['id'], None  # get first element for now

        raise Exception('Invalid status code')
    except Exception as e:
        traceback.print_exc()
        error_msg = f'there was an error getting ingredient id by name {str(e)}'
        log.error(error_msg)
        raise e


def __add_ingredient_ids_to_recipes(recipe: Recipe) -> Recipe:
    ingredients_info = []
    try:
        for ingredient_dict in recipe.ingredients:
            ingredient_id, error = __get_ingredient_id_by_name(ingredient_dict['ingredient_name'])
            if error:
                log.info(f'ingredient {ingredient_dict["ingredient_name"]} doesnt exists')
                return None, True
            else:
                ingredients_info.append({'ingredient_id': ingredient_id,
                                         'amount': ingredient_dict['amount'],
                                         'measure_unit': ingredient_dict['measure_unit'],
                                         'ingredient_name': ingredient_dict['ingredient_name'],
                                         'optional': ingredient_dict['optional']})
    except Exception as e:
        error_msg = 'there was an error making requests [error: {}]'.format(str(e))
        traceback.print_exc()
        log.error(error_msg)
        return None, {'msg': error_msg, 'status_code': 500}

    return ingredients_info, None


def __create_recipes_with_ingredients(recipe, ingredients_info):
    try:
        headers = {'content-type': 'application/json'}
        res = r.post(url=API_ENDPOINT_RECIPES, json=dataclasses.asdict(recipe), headers=headers)
        if res.status_code == 201:
            recipe_id = res.json()['id']
        else:
            return False
    except Exception as e:
        error_msg = 'there was an error making post request for recipe [error: {}]'.format(str(e))
        log.error(error_msg)
        return False

    try:
        url = API_ENDPOINT_RECIPES_INGREDIENTS.format(recipe_id=recipe_id)
        res = r.put(url=url, json=ingredients_info, headers=headers)
        if res.status_code != 200:
            return False
    except Exception as e:
        error_msg = 'there was an error making put request for recipe [error: {}]'.format(str(e))
        log.error(error_msg)
        traceback.print_exc()
        return False

    return True


def read_recipes():
    log.info('going to read recipes input file...')

    recipes = __read_recipes_csv()

    log.info('finished reading recipes input files [recipes:{}]'.format(len(recipes)))

    success_count = 0
    errors_count = 0
    skipped_recipes = []
    for recipe in recipes:
        ingredients_info, error = __add_ingredient_ids_to_recipes(recipe)
        if error:
            # log.debug(f'recipe {recipe.name} have some ingredients that could get their ids. Skipping...')
            skipped_recipes.append(recipe.name)
            continue

        success = __create_recipes_with_ingredients(recipe, ingredients_info)
        if not success:
            log.info(f'Error procesing recipe \'{recipe.name}\'')
            errors_count += 1
        else:
            success_count += 1
        # log.info(f'Finished procesing recipe \'{recipe.name}\'')

    log.info(f'finished making POST requests for recipes [success:{success_count}][errors:{errors_count}][skipped:{len(skipped_recipes)}]')
    log.info(f'skipped recipes: {",".join(skipped_recipes)}')
    return {'msg': 'job finished', 'status_code': 200}, None


def read_ingredients():
    ingredients = []
    log.info('going to read ingredients input file...')

    try:
        with open('ingredients_to_load.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ingredient = dict()
                ingredient['name'] = row['name']
                ingredient['food_group'] = row['food_group']
                ingredient['veggie_friendly'] = bool(row['veggie_friendly'])
                ingredient['storage'] = row['storage']
                ingredient['expiration_time'] = int(row['expiration_time'])
                ingredients.append(ingredient)
    except Exception as e:
        error_msg = 'there was an error reading ingredients to load file [error:{}]'.format(str(e))
        log.error(error_msg)
        return None, {'msg': error_msg, 'status_code': 500}

    log.info('finished reading ingredients input files [recipes:{}]'.format(len(ingredients)))

    success = []
    errors = []
    log.info('going to make POST requests for ingredients...')
    try:
        headers = {'content-type': 'application/json'}
        for ingredient in ingredients:
            res = r.post(url=API_ENDPOINT_INGREDIENTS, json=ingredient, headers=headers)
            if res.status_code == 201:
                success.append(ingredient)
            else:
                errors.append(ingredient)
    except Exception as e:
        error_msg = 'there was an error making requests [error: {}]'.format(str(e))
        log.error(error_msg)
        return None, {'msg': error_msg, 'status_code': 500}

    log.info('finished making POST requests for ingredients [success:{}][errors:{}]'.format(len(success), len(errors)))
    return {'msg': 'job finished', 'status_code': 200}, None
