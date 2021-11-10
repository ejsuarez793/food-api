from sqlalchemy import func
from sqlalchemy.orm import backref
from marshmallow import fields, EXCLUDE, validates_schema, ValidationError

from marshmallow_sqlalchemy import field_for

from app import db
from app import ma

from app.models.ingredients import Ingredient
from app.models.recipes import Recipe

VALID_MEASURE_UNITS = {
    'gr': 'grams',
    'kg': 'kilograms',
    'ml': 'milliliters',
    'l': 'liters',
    'u': 'unit'
}


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    recipe_id = db.Column(db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.ForeignKey('ingredient.id'), primary_key=True)
    ingredients = db.relationship("Ingredient", backref=backref("ingredient"))
    recipes = db.relationship("Recipe", backref=backref("recipe"))

    # extra field of relation
    amount = db.Column(db.Numeric(precision=1000, scale=4, asdecimal=False), nullable=False)
    measure_unit = db.Column(db.String(), nullable=False)
    optional = db.Column(db.Boolean, default=False)

    @staticmethod
    def get_ingredients(recipe_id: str):

        query = db.session.query(Recipe, Ingredient, RecipeIngredient) \
                    .join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id) \
                    .join(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id) \
                    .filter(Recipe.id == recipe_id)

        return query.with_entities(Ingredient.id, Ingredient.name, RecipeIngredient.amount, RecipeIngredient.measure_unit, RecipeIngredient.optional).all()

    @staticmethod
    def get_ingredients_number(recipe_id: str):
        query = db.session.query(func.count(RecipeIngredient.ingredient_id)).filter(
            RecipeIngredient.recipe_id == recipe_id)

        return query.scalar()

    @staticmethod
    def delete_all_ingredients(recipe_id: str):
        # db.session.query()
        query = RecipeIngredient.query.filter(RecipeIngredient.recipe_id == recipe_id)
        return query.delete()

    @staticmethod
    def delete_ingredient(recipe_id: str, ingredient_id):
        # db.session.query()
        query = RecipeIngredient.query\
            .filter(RecipeIngredient.recipe_id == recipe_id)\
            .filter(RecipeIngredient.ingredient_id == ingredient_id)
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


class RecipeIngredientResponseSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    amount = fields.Integer()
    measure_unit = fields.String()
    optional = fields.Boolean()
