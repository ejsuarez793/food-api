from flask_cors import cross_origin
from flask_restx import Resource
from marshmallow import RAISE
from flask import make_response, jsonify

from app.validators.recipes_recommendations import RecipesRecommendationsQueryParser, RecipesRecommendationsQueryParams
from app.repositories import recommendations

rrqp = RecipesRecommendationsQueryParser()


class Recommendation(Resource):

    @cross_origin()
    @rrqp.use_args(RecipesRecommendationsQueryParams(unknown=RAISE), location='query')
    def get(self, params: 'RecipesRecommendationsQueryParams'):
        response, err = recommendations.get_recommendation(params)
        if err:
            return make_response(err, err['status_code'])
        return make_response(jsonify(response), 200)