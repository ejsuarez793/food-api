from marshmallow import fields, EXCLUDE, validates_schema, ValidationError

from app import db, ma
from app.models.pagination import PaginationSchema


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    veggie_friendly = db.Column(db.Boolean(), nullable=False)
    meal_type = db.Column(db.JSON, nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    wash_time = db.Column(db.Integer, nullable=False)
    cook_technique = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)
    info = db.Column(db.JSON, nullable=False)
    steps = db.Column(db.JSON, nullable=False)
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
    def get_by_id(id):
        return Recipe.query.get(id)

    @staticmethod
    def get_by_email(recipe_id):
        return Recipe.query.filter_by(recipe_id=recipe_id).first()

    @staticmethod
    def get_by_date_range(date_from, date_to):
        return Recipe.query.filter(
            Recipe.date_created.between(date_from, date_to)
        ).all()

    @staticmethod
    def get_by_pagination(params):
        page = int((params.offset / params.limit) + 1)
        return Recipe.query.paginate(page, params.limit, False)

    @staticmethod
    def get_by_pagination_and_date_range(params):
        page = int((params.offset / params.limit) + 1)
        return Recipe.query.filter(
            Recipe.date_created.between(params.date_from, params.date_to)
        ).paginate(page, params.limit, False)


class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = (
            False  # Todo: Entender bien esto, si va True pincha el POST
        )
        unknown = EXCLUDE

    @validates_schema
    def validate_types_values(self, data, **kwargs):
        errors = {}
        not_supported_meals = []
        for meal in data['meal_type']:
            if meal not in [
                'breakfast',
                'lunch',
                'dinner',
                'snack',
                'drink',
                'shake',
            ]:  # Todo: dejar esto en una config lista duplicada en otro lado
                not_supported_meals.append(meal)

        if not_supported_meals:
            errors['meal_type'] = [
                '{} \'meal_type\' is not a valid supported meal'.format(
                    ','.join(not_supported_meals)
                )
            ]

        if data['cook_technique'] not in ['batch_cooking', 'single_cooking']:
            errors['cook_technique'] = [
                '{} \'cook_technique\' is not a valid supported cooking technique'.format(
                    data['cook_technique']
                )
            ]

        if errors:
            raise ValidationError(errors)


class RecipePaginationSchema(ma.Schema):
    paging = fields.Nested(PaginationSchema())
    results = fields.Nested(RecipeSchema(), many=True)
