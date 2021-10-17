from app.models.ingredients import VALID_FOOD_GROUPS, VALID_STORAGE_TYPE, VALID_FIELDS

VALID_FIELDS_FOR_SEARCH = VALID_FIELDS

VALID_FILTERS = {
    'eq': ['id', 'name', 'food_group', 'veggie_friendly', 'storage'],
    'ne': ['id', 'food_group', 'veggie_friendly', 'storage'],
    'ilike': ['name'],
    'notilike': ['name'],
    'startswith': ['name'],
    'between': ['date_created', 'expiration_time'],
    'ge': ['date_created', 'expiration_time'],
    'gt': ['date_created', 'expiration_time'],
    'le': ['date_created', 'expiration_time'],
    'lt': ['date_created', 'expiration_time']
}

FILTERS_DATA_TYPES = {
    'integer_values': ['id', 'expiration_time'],
    'real_values': [],
    'discrete_values': {
        'food_group': VALID_FOOD_GROUPS,
        'storage': VALID_STORAGE_TYPE},  # ToDo: pasar esto a una config
    'boolean_values': ['veggie_friendly'],
    'date_values': ['date_created']
}

MAX_MULTIGET_IDS = 20

STR_COLUMNS = ['name', 'food_group', 'storage']

NUMERIC_COLUMNS = ['id', 'expiration_time']
