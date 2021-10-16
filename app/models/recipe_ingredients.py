from sqlalchemy import func
from sqlalchemy.orm import backref
from marshmallow import fields, EXCLUDE, validates_schema, ValidationError

from marshmallow_sqlalchemy import field_for

from app import db
from app import ma

from app.models.ingredients import Ingredient

VALID_MEASURE_UNITS = {
    'gr': 'grams',
    'kg': 'kilograms',
    'ml': 'milliliters',
    'l': 'liters',
    'u': 'unit'
}


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    recipe_id = db.Column(db.ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = db.Column(db.ForeignKey('ingredients.id'), primary_key=True)
    ingredients = db.relationship("Ingredient", backref=backref("ingredient", lazy="joined"))
    recipes = db.relationship("Recipe", backref=backref("recipe", lazy="joined"))

    # extra field of relation
    amount = db.Column(db.Numeric(precision=1000, scale=4, asdecimal=False), nullable=False)
    measure_unit = db.Column(db.String(), nullable=False)

    @staticmethod
    def get_ingredients(recipe_id: str):

        subquery = db.session.query(RecipeIngredient.ingredient_id).filter(RecipeIngredient.recipe_id == recipe_id).subquery()
        query = db.session.query(Ingredient).filter(Ingredient.id.in_(subquery))
        # ToDo: revisar el LEFT OUTER JOIN que hace acá (hace un join y un left outer join)
        # ToDo, no me gusto que tuviera que proyectar RecipeIngredient o ambos, RecipeIngredient
        """query = db.session.query(RecipeIngredient) \
            .join(Ingredient)\
            .filter(RecipeIngredient.recipe_id == recipe_id)"""

        return query.all()

    @staticmethod
    def get_ingredients_number(recipe_id: str):
        query = db.session.query(func.count(RecipeIngredient.ingredient_id)).filter(
            RecipeIngredient.recipe_id == recipe_id)

        return query.scalar()

    @staticmethod
    def delete_all_ingredients(recipe_id: str):
        db.session.query()
        query = RecipeIngredient.query.filter(RecipeIngredient.recipe_id == recipe_id)
        return query.delete()


class RecipeIngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecipeIngredient
        load_instance = False  # Todo: Entender bien esto, si va True pincha el POST
        unknown = EXCLUDE

    ingredient_id = field_for(RecipeIngredient, 'ingredient_id', dump_only=False)
    recipe_id = field_for(RecipeIngredient, 'recipe_id', dump_only=False)

    @validates_schema
    def validate_measure_unit(self, data, **kwargs):
        errors = {}
        # ToDo: pasar esto a config
        measure_unit = data['measure_unit']
        if measure_unit not in VALID_MEASURE_UNITS:
            errors['measure_unit'] = [f'{measure_unit} \'measure_unit\' is not a valid supported measure_unit']

        if errors:
            raise ValidationError(errors)