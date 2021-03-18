"""
Module that have two methods that populates database from csv files
"""

import csv
import logging
from typing import Union, Dict

import requests as r

from requests.exceptions import RequestException

API_ENDPOINT_RECIPES = 'http://localhost:5000/recipes'
API_ENDPOINT_INGREDIENTS = 'http://localhost:5000/ingredients'
log = logging.getLogger(__name__)


def read_recipes() -> Union[Dict, Dict]:
    """
    read_recipes: read recipes from local csv file and then make post
    request to recipe endpoint
    :return: Union of dict with information of the job status,
    if finished correctly or not
    """

    recipes = []
    log.info('going to read recipes input file...')
    recipe_filename = 'recipes_to_load.csv'
    try:
        with open(recipe_filename, 'r') as file:
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
    except ValueError:
        error_msg = 'there was an error reading recipes '\
                    f'to load file [filename:{recipe_filename}]'
        log.exception(error_msg)
        return None, {'msg': error_msg, 'status_code': 500}

    log.info('finished reading recipes input files'
             '[total_recipes:%d]', len(recipes))

    success = []
    errors = []
    log.info('going to make POST requests for recipes...')
    try:
        headers = {'content-type': 'application/json'}
        for recipe in recipes:
            res = r.post(url=API_ENDPOINT_RECIPES,
                         json=recipe,
                         headers=headers)
            if res.status_code == 201:
                success.append(recipe)
            else:
                errors.append(recipe)
    except RequestException:
        error_msg = 'there was an error making post requests'
        log.exception(error_msg)
        return None, {'msg': error_msg, 'status_code': 500}

    log.info('finished making POST requests for recipes '
             '[success:%d][errors:%d]', len(success), len(errors))
    return {'msg': 'job finished', 'status_code': 200}, None


def read_ingredients():
    """
    read_ingredients: read ingredients from local csv file
    and then make post request to ingredients endpoint

    :return: Union of dict with information of the job status,
    if finished correctly or not
    """

    ingredients = []
    log.info('going to read ingredients input file...')
    ingredients_filename = 'ingredients_to_load.csv'
    try:
        with open(ingredients_filename, 'r') as file:
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
    except Exception:
        error_msg = 'there was an error reading ingredients ' \
                    f'to load file [filename:{ingredients_filename}]'
        log.error(error_msg)
        return None, {'msg': error_msg, 'status_code': 500}

    log.info('finished reading ingredients input files '
             '[recipes:%d]', len(ingredients))

    success = []
    errors = []
    log.info('going to make POST requests for ingredients...')
    try:
        headers = {'content-type': 'application/json'}
        for ingredient in ingredients:
            res = r.post(url=API_ENDPOINT_INGREDIENTS,
                         json=ingredient,
                         headers=headers)
            if res.status_code == 201:
                success.append(ingredient)
            else:
                errors.append(ingredient)
    except RequestException:
        error_msg = 'there was an error making post requests'
        log.error(error_msg)
        return None, {'msg': error_msg, 'status_code': 500}

    log.info('finished making POST requests for ingredients '
             '[success:%d][errors:%d]', len(success), len(errors))
    return {'msg': 'job finished', 'status_code': 200}, None
