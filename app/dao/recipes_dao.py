from sqlalchemy import text

from app import db

COLUMNS = ['id','name', 'veggie_friendly', 'meal_type', 'cook_time', 'wash_time', 'cook_technique', 'ingredients', 'info', 'steps']
QUERY = "SELECT {columns} FROM recipes WHERE id in(SELECT id FROM unnest(meal_type) mt WHERE mt in ({meals_type}))";
QUERY_VEGGIE_ONLY = "SELECT {columns} FROM recipes WHERE id in(SELECT id FROM unnest(meal_type) mt WHERE mt in ({meals_type})) AND veggie_friendly = true";

def get_recommendations(veggie_only: bool, meals: list):
    base_query = QUERY_VEGGIE_ONLY if veggie_only else QUERY
    query = base_query.format(columns=','.join(COLUMNS), meals_type=','.join(['\'{}\''.format(meal) for meal in meals]))
    print(query)
    result = db.engine.execute(query)
    recipes = []
    for row in result:
        recipes.append(dict(zip(COLUMNS, row)))
    return recipes
