from flask import request, make_response
from flask_restx import Resource

from webargs import fields
from webargs.flaskparser import use_args
from marshmallow import RAISE
from app.repositories import ingredients

from app.validators.ingredients import IngredientSearchQuery, IngredientQueryParser

ingredient_query_parser = IngredientQueryParser()


class Ingredient(Resource):
    @ingredient_query_parser.use_args(IngredientSearchQuery(unknown=RAISE), location='query')
    def get(self, params: 'IngredientSearchQuery'):
        response, error = ingredients.search(params)
        if error:
            return error, error['status_code']
        return response, 200

    def post(self):
        json_data = request.get_json()
        response, err = ingredients.create(json_data)
        if err:
            return make_response(err, err['status_code'])
        return make_response(response, 201)


class IngredientById(Resource):
    def get(self, id: int):
        response, error = ingredients.get(id)
        if error:
            return make_response(error, error['status_code'])
        return response, 200

    def put(self):
        pass

    def delete(self, id: int):
        response, err = ingredients.delete(id)
        if err:
            return err, err['status_code']
        return make_response(response, 204)

