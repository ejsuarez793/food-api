import logging
from app import db

log = logging.getLogger(__name__)

COLUMNS = ['id', 'name', 'veggie_friendly', 'meal_type', 'cook_time', 'wash_time', 'cook_technique', 'info', 'steps']
QUERY = "SELECT {columns} FROM recipe WHERE id in(SELECT id FROM unnest(meal_type) mt WHERE mt in ({meals_type}))";
QUERY_VEGGIE_ONLY = "SELECT {columns} FROM recipe WHERE id in(SELECT id FROM unnest(meal_type) mt WHERE mt in ({meals_type})) AND veggie_friendly = true";


def get_recommendation(veggie_only: bool, meals: list):
    base_query = QUERY_VEGGIE_ONLY if veggie_only else QUERY
    query = base_query.format(columns=','.join(COLUMNS), meals_type=','.join(['\'{}\''.format(meal) for meal in meals]))

    try:
        result = db.engine.execute(query)
    except Exception as e:
        log.error('there was a database error getting recipes [error:{}]'.format(str(e)))
        raise e

    recipes = {}
    for meal in meals:
        recipes[meal] = []

    for row in result:
        recipe = dict(zip(COLUMNS, row))
        for rmp in recipe['meal_type']:
            if rmp not in meals:
                continue
            recipes[rmp].append(recipe)

    return recipes
