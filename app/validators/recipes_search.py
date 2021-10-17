from app.models.recipes import VALID_COOKING_TECHNIQUES, VALID_MEAL_TYPES, VALID_FIELDS


MAX_MULTIGET_IDS = 20

# ToDo revisar posible referencia circular?
VALID_FIELDS_FOR_SEARCH = VALID_FIELDS

VALID_FILTERS = {
    'eq': ['id', 'name', 'veggie_friendly', 'meal_type', 'cook_technique'],
    'ne': ['id', 'veggie_friendly', 'meal_type', 'cook_technique'],
    'ilike': ['name'],
    'notilike': ['name'],
    'startswith': ['name'],
    'between': ['date_created', 'expiration_time', 'cook_time', 'wash_time'],
    'ge': ['date_created', 'expiration_time', 'cook_time', 'wash_time'],
    'gt': ['date_created', 'expiration_time', 'cook_time', 'wash_time'],
    'le': ['date_created', 'expiration_time', 'cook_time', 'wash_time'],
    'lt': ['date_created', 'expiration_time', 'cook_time', 'wash_time']
}

FILTERS_DATA_TYPES = {
    'integer_values': ['expiration_time', 'cook_time', 'wash_time'],
    'real_values': [],
    'discrete_values': {
        'meal_type': VALID_MEAL_TYPES,
        'cook_technique': VALID_COOKING_TECHNIQUES},
    'boolean_values': ['veggie_friendly'],
    'date_values': ['date_created']
}

STR_COLUMNS = ['id', 'name', 'meal_type', 'cook_technique']

NUMERIC_COLUMNS = ['expiration_time', 'cook_time', 'wash_time']
