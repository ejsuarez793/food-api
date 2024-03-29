from app import db
from app import ma

from marshmallow import fields, EXCLUDE, validates_schema, ValidationError

from sqlalchemy import func

from app.models.pagination import PaginationSchema

VALID_FOOD_GROUPS = ['dairies', 'proteins', 'fruits', 'vegetables', 'fats', 'grains', 'sweets', 'condiments', 'waters']
VALID_STORAGE_TYPE = ['dry', 'refrigerated', 'frozen']

# valid fields for 'fields' query param
VALID_FIELDS = {
    'id',
    'name',
    'food_group',
    'veggie_friendly',
    'storage',
    'expiration_time',
    'date_created',
    'last_updated'
}


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    food_group = db.Column(db.String(), nullable=False)
    veggie_friendly = db.Column(db.Boolean(), nullable=False)
    storage = db.Column(db.String(), nullable=False)
    expiration_time = db.Column(db.Interval(native=True), nullable=False)  ## native=True supports Postgrseslq and Oracle native type
    date_created = db.Column(db.TIMESTAMP, default=db.func.now(), onupdate=db.func.current_timestamp())
    last_updated = db.Column(db.TIMESTAMP, default=db.func.now(), onupdate=db.func.current_timestamp())

    @staticmethod
    def get_by_id(id, fields=None):
        query = Ingredient.query

        if fields is not None:
            query = query.with_entities(*fields)

        return query\
            .filter(Ingredient.id == id)\
            .first()

    @staticmethod
    def multiget(ids, fields):
        query = Ingredient.query

        if fields is not None:
            query = query.with_entities(*fields)

        return query\
            .filter(Ingredient.id.in_(ids))\
            .all()

    @staticmethod
    def search(params):
        query = Ingredient.query

        # had to implement this 'with_entities' one diff than two methods above
        entities_list = []
        if params.fields is not None:
            for field in params.fields:
                entities_list.append(getattr(Ingredient, field))
            query = query.with_entities(*tuple(entities_list))

        for f in params.filters:
            field = f['field']
            operator = f['operator']
            value = f['value']
            if operator == 'eq':
                query = query.filter(getattr(Ingredient, field) == value)
            elif operator == 'ne':
                query = query.filter(getattr(Ingredient, field) != value)
            elif operator == 'ilike':
                query = query.filter(getattr(Ingredient, field).ilike(f'%{value}%'))
            elif operator == 'notilike':
                query = query.filter(~getattr(Ingredient, field).ilike(f'%{value}%'))
            elif operator == 'startswith':
                query = query.filter(getattr(Ingredient, field).ilike(f'{value}%'))
            elif operator == 'ge':
                query = query.filter(getattr(Ingredient, field) >= value)
            elif operator == 'gt':
                query = query.filter(getattr(Ingredient, field) > value)
            elif operator == 'le':
                query = query.filter(getattr(Ingredient, field) <= value)
            elif operator == 'lt':
                query = query.filter(getattr(Ingredient, field) < value)
            elif operator == 'between':
                _from = value.split(',')[0]  # ToDo: sacar esta lógica de aquí?
                _to = value.split(',')[1]  # ToDo: sacar esta lógica de aquí?
                query = query.filter(getattr(Ingredient, field).between(_from, _to))

        if params.sort_by is not None:
            sort_by_func = getattr(Ingredient, params.sort_by)
            if params.str_sort:
                sort_by_func = func.lower(getattr(Ingredient, params.sort_by))

            sort_by_asc_func = sort_by_func.asc()
            if params.asc is False:
                sort_by_asc_func = sort_by_func.desc()

            query = query.order_by(sort_by_asc_func)

        page = int((params.offset / params.limit) + 1)
        return query.paginate(page, params.limit, False)


class IngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingredient
        load_instance = False  # Todo: Entender bien esto, si va True pincha el POST
        unknown = EXCLUDE

    @validates_schema
    def validate_food_group(self, data, **kwargs):
        errors = {}
        partial = kwargs['partial']
        # ToDo: pasar esto a config
        if 'food_group' in data:
            if data['food_group'] not in VALID_FOOD_GROUPS:
                errors['food_group'] = ['{food_group} \'food_group\' is not a valid supported food group'.format(food_group=data['food_group'])]
        elif not partial:
            errors['food_group'] = ['attribute \'food_group\' is required']

        # ToDo: pasar esto a config
        if 'storage' in data:
            if data['storage'] not in VALID_STORAGE_TYPE:
                errors['storage'] = ['{storage} \'storage\' is not a valid supported storage type'.format(storage=data['storage'])]
        elif not partial:
            errors['storage'] = ['attribute \'storage\' is required']

        if errors:
            raise ValidationError(errors)


class IngredientPaginationSchema(ma.Schema):
    paging = fields.Nested(PaginationSchema())
    results = fields.Nested(IngredientSchema(), many=True)