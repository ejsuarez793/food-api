

from app.dao import summaries_dao


def get_summary(recipe_ids: list):
    return summaries_dao.get_ingredients_summary(recipe_ids), None