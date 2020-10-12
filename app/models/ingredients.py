from app import db
from app import ma

from marshmallow import fields, EXCLUDE, validates_schema, ValidationError

from app.models.pagination import PaginationSchema


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    food_group = db.Column(db.String(), nullable=False)
    veggie_friendly = db.Column(db.Boolean(), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=4, asdecimal=False), nullable=False)
    currency = db.Column(db.String(), nullable=False)
    storage = db.Column(db.String(), nullable=False)
    expiration_time = db.Column(db.Interval(native=True), nullable=False)  ## native=True supports Postgrseslq and Oracle native type
    date_created = db.Column(db.TIMESTAMP, default=db.func.now(), onupdate=db.func.current_timestamp())
    last_updated = db.Column(db.TIMESTAMP, default=db.func.now(), onupdate=db.func.current_timestamp())

    @staticmethod
    def get_by_id(id):
        return Ingredient.query.get(id)

    @staticmethod
    def multiget(ids):
        return Ingredient.query.filter(Ingredient.id.in_(ids)).all()


class IngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingredient
        load_instance = False  # Todo: Entender bien esto, si va True pincha el POST
        unknown = EXCLUDE

    @validates_schema
    def validate_food_group(self, data, **kwargs):
        errors = {}
        if data['food_group'] not in ['dairies', 'proteins', 'fruits', 'vegetables', 'fats', 'grains', 'sweets', 'condiments']:
            errors['food_group'] = ['{food_group} \'food_group\' is not a valid supported meal'.format(food_group=data['food_group'])]

        if data['storage'] not in ['dry', 'refrigerated', 'frozen']:
            errors['storage'] = ['{storage} \'storage\' is not a valid supported meal'.format(storage=data['storage'])]

        if errors:
            raise ValidationError(errors)


class IngredientPaginationSchema(ma.Schema):
    paging = fields.Nested(PaginationSchema())
    results = fields.Nested(IngredientSchema(), many=True)