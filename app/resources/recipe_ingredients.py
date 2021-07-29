from flask import request, make_response

from flask_restx import Resource

from app.repositories import recipe_ingredients


class RecipeIngredientById(Resource):

    def get(self, recipe_id: str):
        response, err = recipe_ingredients.get_recipe_with_ingredients(recipe_id)
        if err:
            return err, err['status_code']
        return response, 200


    def post(self, recipe_id: str):
        json_data = request.get_json()
        response, err = recipe_ingredients.add_ingredients_to_recipe(recipe_id, json_data)
        if err:
            return err, err['status_code']
        return response, 201  # ToDo: revisar que status code sería correcto en este caso

    def put(self):
        pass

    def delete(self):
        pass
