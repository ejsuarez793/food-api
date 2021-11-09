from abc import ABC, abstractmethod
from typing import Dict

from random import seed
from random import randint
from datetime import datetime

class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Recommendation algorithm uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def do_algorithm(self, recipes: Dict, params: Dict) -> Dict:
        pass


"""
Concrete Strategies implement the algorithm while following the base Strategy
interface. The interface makes them interchangeable in the Context.
"""


class SimpleRecommendationStrategy(Strategy):
    def do_algorithm(self, recipes: Dict, params: Dict) -> Dict:
        recommendation = {}
        for day in range(0, params.days):
            day_key = 'day_' + str(day)
            recommendation[day_key] = {}
            for meal_type in params.meals:
                recommendation[day_key][meal_type] = []

        seed(datetime.now())  # for choice function below
        for day in range(0, params.days):
            day_key = 'day_' + str(day)
            for meal_type in params.meals:
                if recipes[meal_type]:
                    enoughMealTypesForAllDays = len(recipes[meal_type]) >= params.days
                    index = randint(0, len(recipes[meal_type]) - 1)
                    recommendation[day_key][meal_type] = recipes[meal_type].pop(index) if \
                        enoughMealTypesForAllDays else recipes[meal_type][index]

        return recommendation