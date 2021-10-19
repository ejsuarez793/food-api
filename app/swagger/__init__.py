ERROR_MSG = {
          "type": "object",
          "properties": {
            "msg": {
              "type": "string",
              "description": "Message of the error"
            },
            "status_code": {
              "type": "integer",
              "description": "status code returned in response"
            }
          }
        }

PAGINATION = {
    "type": "object",
    "properties": {
        "offset": {
            "type": "integer",
            "description": "offset of search"
        },
        "limit": {
            "type": "integer",
            "description": "limit of search"
        },
        "total": {
            "type": "integer",
            "description": "total results of search"
        }
    }
}

INGREDIENT = {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer",
              "description": "The id of the ingredient"
            },
            "name": {
              "type": "string",
              "description": "The name of the ingredient"
            },
            "veggie_friendly": {
              "type": "boolean",
              "description": "if the ingredient is vegetarian friendly"
            },
            "food_group": {
              "type": "string",
              "enum": ['dairies', 'proteins', 'fruits', 'vegetables', 'fats', 'grains', 'sweets', 'condiments', 'waters'],
              "description": "food group in which the ingredient falls in"
            },
            "storage": {
              "type": "string",
              "enum": ['dry', 'refrigerated', 'frozen'],
              "description": "indicates how the ingredient will need to be storage"
            },
            "expiration_time": {
              "type": "integer",
              "description": "time of duration of the ingredient before it expires (in days)"
            },
            "date_created": {
              "type": "string",
              "description": "timestamp of recipe creation"
            },
            "last_updated": {
              "type": "string",
              "description": "timestamp of recipe last update"
            }
          }
        }

INGREDIENT_SEARCH = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/Ingredient"
            }
        },
        "pagination": {
            "type": "object",
            "schema": {"$ref": "#/definitions/Pagination"}
        }
    }
}

RECIPE = {
          "type": "object",
          "properties": {
            "id": {
              "type": "string",
              "description": "The id of the recipe"
            },
            "name": {
              "type": "string",
              "description": "The name of the recipe"
            },
            "veggie_friendly": {
              "type": "boolean",
              "description": "if recipe is vegetarian friendly"
            },
            "meal_type": {
              "type": "string",
              "enum": ['lunch', 'dinner', 'breakfast', 'snack', 'shake'],
              "description": "category of meal type in which recipes falls in"
            },
            "cook_technique": {
              "type": "string",
              "enum": ['batch_cooking', 'single_cooking'],
              "description": "indicates if recipe is meant for one meal or for several meals in which case you need to storage it for latter days"
            },
            "wash_time": {
              "type": "integer",
              "description": "estimated time needed to wash all things used during the recipe making (in minutes)"
            },
            "cook_time": {
              "type": "integer",
              "description": "estimated time needed to cook recipe (in minutes)"
            },
            "date_created": {
              "type": "string",
              "description": "timestamp of recipe creation"
            },
            "last_updated": {
              "type": "string",
              "description": "timestamp of recipe last update"
            },
            "info": {
              "type": "object",
              "description": "information about the recipe"
            },
            "steps": {
              "type": "object",
              "description": "steps of the recipe"
            }
          }
        }

RECIPE_SEARCH = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/Recipe"
            }
        },
        "pagination": {
            "type": "object",
            "schema": {"$ref": "#/definitions/Pagination"}
        }
    }
}

RECIPE_BY_ID = {
          "type": "object",
          "properties": {
            "id": {
              "type": "string",
              "description": "The id of the recipe"
            },
            "name": {
              "type": "string",
              "description": "The name of the recipe"
            },
            "veggie_friendly": {
              "type": "boolean",
              "description": "if recipe is vegetarian friendly"
            },
            "meal_type": {
              "type": "string",
              "enum": ['lunch', 'dinner', 'breakfast', 'snack', 'shake'],
              "description": "category of meal type in which recipes falls in"
            },
            "cook_technique": {
              "type": "string",
              "enum": ['batch_cooking', 'single_cooking'],
              "description": "indicates if recipe is meant for one meal or for several meals in which case you need to storage it for latter days"
            },
            "wash_time": {
              "type": "integer",
              "description": "estimated time needed to wash all things used during the recipe making (in minutes)"
            },
            "cook_time": {
              "type": "integer",
              "description": "estimated time needed to cook recipe (in minutes)"
            },
            "date_created": {
              "type": "string",
              "description": "timestamp of recipe creation"
            },
            "last_updated": {
              "type": "string",
              "description": "timestamp of recipe last update"
            },
            "info": {
              "type": "object",
              "description": "information about the recipe"
            },
            "steps": {
              "type": "object",
              "description": "steps of the recipe"
            },
            "ingredients":{
                "type": "array",
                "description": "list of ingredients associated with recipe, with their amount and measure unit",
                "items": {
                    "$ref": "#/definitions/RecipeIngredient"
                }
            }
          }
        }

RECIPE_INGREDIENT = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "description": "the id of the ingredient"
        },
        "name": {
            "type": "string",
            "description": "The name of the ingredient"
        },
        "measure_unit": {
          "type": "string",
          "description": "measure unit for ingredient quantity"
        },
        "amount": {
          "type": "string",
          "description": "amount of ingredient to use in recipe"
        },
        "optional":{
              "type": "boolean",
              "description": "indicates if ingredient is optional or not"
        }
      }
}

RECIPE_INGREDIENT_PUT = {
    "type": "object",
    "properties": {
        "ingredient_id": {
            "type": "integer",
            "description": "the id of the ingredient"
        },
        "measure_unit": {
          "type": "string",
          "description": "measure unit for ingredient quantity"
        },
        "amount": {
          "type": "string",
          "description": "amount of ingredient to use in recipe"
        },
        "optional":{
              "type": "boolean",
              "description": "indicates if ingredient is optional or not"
        }
      }
}


DEFINITIONS = {
    "ErrorMsg": ERROR_MSG,
    "Pagination": PAGINATION,
    "Ingredient": INGREDIENT,
    "IngredientSearch": INGREDIENT_SEARCH,
    "Recipe": RECIPE,
    "RecipeSearch": RECIPE_SEARCH,
    "RecipeById": RECIPE_BY_ID,
    "RecipeIngredient": RECIPE_INGREDIENT,
    "RecipeIngredientPut": RECIPE_INGREDIENT_PUT
}



####### SEARCH PARAMETERS

SEARCH_PARAMETERS = [
    {
        "name": "ids",
        "in": "query",
        "type": "str",
        "description": "ids to search separated by comma (max ids is 20). if set all other parameters are ignored",
    },
    {
        "name": "fields",
        "in": "query",
        "type": "string",
        "description": "fields needed in response separated by comma. e.g: id,name,veggie_friendly"
    },
    {
        "name": "offset",
        "in": "query",
        "type": "integer",
        "description": "offset for result pagination",
        "default": "0"
    },
    {
        "name": "limit",
        "in": "query",
        "type": "integer",
        "description": "limit for result pagination (max_limit is 10)",
        "default": "10"
    },
    {
        "name": "sort_by",
        "in": "query",
        "type": "string",
        "description": "field to sort by in search"
    },
    {
        "name": "asc",
        "in": "query",
        "type": "boolean",
        "description": "if true sorting will be ascending by \'sort_by\' field, false otherwise",
        "default": "true"
    }
]



##### ERROR_MSG

ERROR_RESPONSE = {
  "description": "not found msg | validation error msg | server error message",
  "schema": {"$ref": "#/definitions/ErrorMsg"}
}