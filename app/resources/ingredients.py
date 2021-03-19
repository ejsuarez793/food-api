from flask import request, make_response
from flask_restx import Resource

from webargs import fields
from webargs.flaskparser import use_args

from app.repositories import ingredients


class Ingredient(Resource):
    # Todo: hace falta el use_args para un parámetro tan simple?
    #  sobretodo si el error de validación no lo puedo capturar dentro del get
    @use_args({'ids': fields.DelimitedList(fields.Str())}, location='query')
    def get(self, args):
        ids = args['ids']
        response, error = ingredients.multiget(ids)
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
