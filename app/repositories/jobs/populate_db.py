import csv
import logging
import requests as r

API_ENDPOINT_RECIPES = 'http://localhost:5000/recipes'
API_ENDPOINT_INGREDIENTS = 'http://localhost:5000/ingredients'
log = logging.getLogger(__name__)


def read_recipes():
    recipes = []
    log.info('going to read recipes input file...')

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
                recipe['ingredients'] = row['ingredients']
                recipe['info'] = row['info']
                recipe['steps'] = row['steps']
                recipes.append(recipe)
    except Exception as e:
        error_msg = 'there was an error reading recipes to load file [error:{}]'.format(str(e))
        log.error(error_msg)
        return None, {'msg': error_msg, 'status_code': 500}

    log.info('finished reading recipes input files [recipes:{}]'.format(len(recipes)))

    success = []
    errors = []
    log.info('going to make POST requests for recipes...')
    try:
        headers = {'content-type': 'application/json'}
        for recipe in recipes:
            res = r.post(url=API_ENDPOINT_RECIPES, json=recipe, headers=headers)
            if res.status_code == 201:
                success.append(recipe)
            else:
                errors.append(recipe)
    except Exception as e:
        error_msg = 'there was an error making requests [error: {}]'.format(str(e))
        log.error(error_msg)
        return None, {'msg': error_msg, 'status_code': 500}

    log.info('finished making POST requests for recipes [success:{}][errors:{}]'.format(len(success), len(errors)))
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
                ingredient['price'] = float(row['price'])
                ingredient['currency'] = row['currency']
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
