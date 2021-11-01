import logging
from dataclasses import dataclass
from decimal import Decimal

from webargs.flaskparser import FlaskParser
from werkzeug.exceptions import BadRequest

from marshmallow import fields, post_load, Schema, ValidationError

log = logging.getLogger(__name__)

@dataclass
class RecipesRecommendationsParams:
    days: int
    # snacks_number: int
    meals: list
    time: int
    veggie_only: bool


class RecipesRecommendationsQueryParams(Schema):
    days = fields.Integer()
    # snacks_number = fields.Integer()
    meals = fields.List(fields.String())
    time = fields.Integer()
    veggie_only = fields.Boolean()

    @post_load
    def make_object(self, data, **kwargs):
        return RecipesRecommendationsParams(**data)


class RecipesRecommendationsQueryParser(FlaskParser):
    def load_querystring(self, req, schema):
        return _validate_params(req, schema)

    def handle_error(self, error, req, schema, error_status_code, error_headers):
        raise BadRequest(error.messages)


def _validate_params(request, schema):
    try:
        days = int(request.args.get('days')) if request.args.get('days') is not None else 1
        # snacks_number = int(request.args.get('snacks_number')) if request.args.get('snacks_number') is not None else 0
        meals = request.args.get('meals').split(',') if request.args.get('meals') is not None else ['breakfast', 'lunch', 'dinner', 'snack', 'shake']
        time = int(request.args.get('time')) if request.args.get('time') is not None else 0
        veggie_only = bool(request.args.get('veggie_only')) if request.args.get('veggie_only') is not None else False
    except Exception as e:
        log.error('there was an error parsing params [error:{}]'.format(str(e)))
        raise ValidationError('there was an error parsing params. please check data types')

    errors = {}
    if days < 0 or days > 7:
        errors['days'] = 'param \'days\' is not between 0 and 7'

    # if snacks_number < 0 or snacks_number > 2:
    #     errors['snacks_number'] = 'param \'snacks_number\' is not between 0 and 2'

    for meal in meals:
        if meal not in ['breakfast', 'lunch', 'dinner', 'snack', 'drink', 'shake']:  # Todo: dejar esto en una config lista duplicada en otro lado
            errors['meals'] = 'param \'meals\' contains a value not supported for a meal'
            continue

    if time < 0 and time > 450: # 450 minutes is 7.5 hours of cooking + washing
        errors['time'] = 'param \'time\' is not between 0 and 450'

    if errors:
        raise ValidationError(errors)

    params = dict(days=days, meals=meals, time=time, veggie_only=veggie_only)
    return params
