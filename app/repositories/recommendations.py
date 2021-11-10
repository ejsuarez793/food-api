import logging

from app.dao import recommendations_dao

from app.recommendations_algoritms.recommendation_algorithm import RecommendationAlgorithm
from app.recommendations_algoritms.strategies.strategies import SimpleRecommendationStrategy

recommendation_algorithm = RecommendationAlgorithm(SimpleRecommendationStrategy())
log = logging.getLogger(__name__)


def get_recommendation(params):
    try:
        recipes = recommendations_dao.get_recommendation(params.veggie_only, params.meals)
    except Exception as e:
        log.error('there was an error getting recommendations from recipe dao [error:{}]'.format(str(e)))
        return None, {'msg': 'there was an error getting recommendations', 'status_code': 500}

    try:
        response = recommendation_algorithm.do_recommendation(recipes, params)
    except Exception as e:
        log.error('there was an error preparing recommendation [error:{}]'.format(str(e)))
        return None, {'msg': 'there was an error getting recommendations', 'status_code': 500}

    return response, None

