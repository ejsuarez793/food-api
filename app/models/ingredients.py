"""
This module defines the database sqlalchemy orm model for ingredients
"""

from marshmallow import fields, EXCLUDE, validates_schema, ValidationError

from app import db, ma
from app.models.pagination import PaginationSchema


class Ingredient(db.Model):
    """
    Ingredient model
    """

    __tablename__ = 'ingredients'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    food_group = db.Column(db.String(), nullable=False)
    veggie_friendly = db.Column(db.Boolean(), nullable=False)
    price = db.Column(
        db.Numeric(precision=10, scale=4, asdecimal=False), nullable=False
    )
    currency = db.Column(db.String(), nullable=False)
    storage = db.Column(db.String(), nullable=False)
    expiration_time = db.Column(
        db.Interval(native=True), nullable=False
    )  ## native=True supports Postgrseslq and Oracle native type
    date_created = db.Column(
        db.TIMESTAMP,
        default=db.func.now(),
        onupdate=db.func.current_timestamp(),
    )
    last_updated = db.Column(
        db.TIMESTAMP,
        default=db.func.now(),
        onupdate=db.func.current_timestamp(),
    )

    @staticmethod
    def get_by_id(ingredient_id: int):
        """
        get by id static method
        :param id: ingredient id int param
        :return: query result for id param
        """

        return Ingredient.query.get(ingredient_id)

    @staticmethod
    def multiget(ids):
        """
        multiget id
        :param ids: ids int list
        :return: query result for id list
        """

        return Ingredient.query.filter(Ingredient.id.in_(ids)).all()


class IngredientSchema(ma.SQLAlchemyAutoSchema):
    """
    Ingredient Schema used to serializa and deserialize an Ingredient
    """

    class Meta:
        model = Ingredient
        load_instance = (
            False  # Todo: Entender bien esto, si va True pincha el POST
        )
        unknown = EXCLUDE

    @validates_schema
    def validate_food_group(self, data, **kwargs):
        """
        validate that food group and storage params are in within certain values
        :param data: dict with data of the ingredient for creation
        :param kwargs:
        :return: raise exception on errors
        """
        errors = {}
        if data['food_group'] not in [
            'dairies',
            'proteins',
            'fruits',
            'vegetables',
            'fats',
            'grains',
            'sweets',
            'condiments',
        ]:
            errors['food_group'] = [
                f'{data["food_group"]} \'food_group\' is not a valid ' 
                'supported meal'
            ]

        if data['storage'] not in ['dry', 'refrigerated', 'frozen']:
            errors['storage'] = [
                f'{data["storage"]} \'storage\' is not a valid supported meal'
            ]

        if errors:
            raise ValidationError(errors)


class IngredientPaginationSchema(ma.Schema):
    """
    Ingredient Pagination Schema for pagination query response
    """

    paging = fields.Nested(PaginationSchema())
    results = fields.Nested(IngredientSchema(), many=True)
