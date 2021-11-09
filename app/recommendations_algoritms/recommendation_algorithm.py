from __future__ import annotations
from typing import Dict

from app.recommendations_algoritms.strategies.strategies import Strategy


class RecommendationAlgorithm:
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def do_recommendation(self, recipes: Dict, params: Dict) -> Dict:
        return self._strategy.do_algorithm(recipes, params)
