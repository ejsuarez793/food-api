"""
Ingredient Resources
"""

from flask import request, make_response
from flask_restx import Resource

from webargs import fields
from webargs.flaskparser import use_args

from app.repositories import ingredients


class Ingredient(Resource):
    """
    Ingredient Resource for general CRUD methods
    """

    # Todo: hace falta el use_args para un parámetro tan simple?
    #  sobretodo si el error de validación no lo puedo capturar dentro del get
    @use_args({'ids': fields.DelimitedList(fields.Str())}, location='query')
    def get(self, args):
        """
        get ingredients using multi-get
        :param args: dict with query params
        :return: ingredients that match ids passed
        """

        ids = args['ids']
        response, error = ingredients.multiget(ids)
        if error:
            return error, error['status_code']
        return response, 200

    def post(self):
        """
        post that allows ingredient creation
        :return: newly created ingredient on success and error otherwise
        """

        json_data = request.get_json()
        response, err = ingredients.create(json_data)
        if err:
            return make_response(err, err['status_code'])
        return make_response(response, 201)


class IngredientById(Resource):
    """
    IngredientById Resource, used to methods that allow id-based operations
    """

    def get(self, ingredient_id: int):
        """
        get method by id
        :param ingredient_id: integer representing ingredient id
        :return: ingredient if found and not found or error otherwise
        """

        response, error = ingredients.get(ingredient_id)
        if error:
            return make_response(error, error['status_code'])
        return response, 200

    def put(self):
        """
        put method
        :return:
        """
        # ToDo: implementar este metodo y actualizar docstring
        pass

    def delete(self, ingredient_id: int):
        """
        delete method by id
        :param ingredient_id:
        :return: 204 on success and error otherwise
        """

        response, err = ingredients.delete(ingredient_id)
        if err:
            return err, err['status_code']
        return make_response(response, 204)
