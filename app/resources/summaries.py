from flask import make_response, jsonify
from flask_cors import cross_origin
from flask_restx import Resource
from webargs.flaskparser import parser
from webargs import fields

from app.repositories import summaries


class Summary(Resource):

    @cross_origin()
    @parser.use_args({"recipe_ids": fields.DelimitedList(fields.Str())})
    def post(self, recipe_ids):
        print(recipe_ids)
        response, err = summaries.get_summary(recipe_ids['recipe_ids'])
        if err:
            return make_response(err, err['status_code'])
        return make_response(jsonify(response), 200)