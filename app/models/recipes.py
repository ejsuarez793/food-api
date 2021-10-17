from app import db
from app import ma

from marshmallow import fields, EXCLUDE, validates_schema, ValidationError
from sqlalchemy import func

from app.models.pagination import PaginationSchema

VALID_MEAL_TYPES = ['breakfast', 'lunch', 'dinner', 'snack', 'drink', 'shake']
VALID_COOKING_TECHNIQUES = ['batch_cooking', 'single_cooking']

VALID_FIELDS = {
    'id',
    'name',
    'veggie_friendly',
    'meal_type',
    'cook_time',
    'wash_time',
    'cook_technique',
    'info',
    'steps',
    'date_created',
    'last_updated'
}


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    veggie_friendly = db.Column(db.Boolean, nullable=False)
    meal_type = db.Column(db.ARRAY(db.String), nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    wash_time = db.Column(db.Integer, nullable=False)
    cook_technique = db.Column(db.String, nullable=False)
    info = db.Column(db.JSON, nullable=False)
    steps = db.Column(db.JSON, nullable=False)
    date_created = db.Column(db.TIMESTAMP, default=db.func.now(), onupdate=db.func.current_timestamp())
    last_updated = db.Column(db.TIMESTAMP, default=db.func.now(), onupdate=db.func.current_timestamp())

    @staticmethod
    def get_by_id(id, fields=None):
        query = Recipe.query

        if fields is not None:
            query = query.with_entities(*fields)

        return query \
            .filter(Recipe.id == id) \
            .first()

    @staticmethod
    def multiget(ids, fields):
        query = Recipe.query

        if fields is not None:
            query = query.with_entities(*fields)

        return query \
            .filter(Recipe.id.in_(ids)) \
            .all()

    @staticmethod
    def search(params):
        query = Recipe.query

        # had to implement this 'with_entities' one diff than two methods above
        entities_list = []
        if params.fields is not None:
            for field in params.fields:
                entities_list.append(getattr(Recipe, field))
            query = query.with_entities(*tuple(entities_list))

        for f in params.filters:
            field = f['field']
            operator = f['operator']
            value = f['value']
            if operator == 'eq':
                query = query.filter(getattr(Recipe, field) == value)
            elif operator == 'ne':
                query = query.filter(getattr(Recipe, field) != value)
            elif operator == 'ilike':
                query = query.filter(getattr(Recipe, field).ilike(f'%{value}%'))
            elif operator == 'notilike':
                query = query.filter(~getattr(Recipe, field).ilike(f'%{value}%'))
            elif operator == 'startswith':
                query = query.filter(getattr(Recipe, field).ilike(f'{value}%'))
            elif operator == 'ge':
                query = query.filter(getattr(Recipe, field) >= value)
            elif operator == 'gt':
                query = query.filter(getattr(Recipe, field) > value)
            elif operator == 'le':
                query = query.filter(getattr(Recipe, field) <= value)
            elif operator == 'lt':
                query = query.filter(getattr(Recipe, field) < value)
            elif operator == 'between':
                _from = value.split(',')[0]  # ToDo: sacar esta lógica de aquí?
                _to = value.split(',')[1]  # ToDo: sacar esta lógica de aquí?
                query = query.filter(getattr(Recipe, field).between(_from, _to))

        if params.sort_by is not None:
            sort_by_func = getattr(Recipe, params.sort_by)
            if params.str_sort:
                sort_by_func = func.lower(getattr(Recipe, params.sort_by))

            sort_by_asc_func = sort_by_func.asc()
            if params.asc is False:
                sort_by_asc_func = sort_by_func.desc()

            query = query.order_by(sort_by_asc_func)

        page = int((params.offset / params.limit) + 1)
        return query.paginate(page, params.limit, False)


class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = False  # Todo: Entender bien esto, si va True pincha el POST
        unknown = EXCLUDE

    @validates_schema
    def validate_types_values(self, data, **kwargs):
        errors = {}
        not_supported_meals = []
        for meal in data['meal_type']:
            if meal not in VALID_MEAL_TYPES:  # Todo: dejar esto en una config lista duplicada en otro lado
                not_supported_meals.append(meal)

        if not_supported_meals:
            errors['meal_type'] = ['{} \'meal_type\' is not a valid supported meal'.format(','.join(not_supported_meals))]

        if data['cook_technique'] not in VALID_COOKING_TECHNIQUES:
            errors['cook_technique'] = ['{} \'cook_technique\' is not a valid supported cooking technique'.format(data['cook_technique'])]

        if errors:
            raise ValidationError(errors)


class RecipePaginationSchema(ma.Schema):
    paging = fields.Nested(PaginationSchema())
    results = fields.Nested(RecipeSchema(), many=True)

