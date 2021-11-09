from app.swagger import DEFINITIONS, ERROR_RESPONSE

recipe_by_id_ingredient_get = {
    "description": "endpoint to retrieve recipe and its ingredients by recipe id",
    "parameters": [
        {
            "name": "recipe_id",
            "in": "path",
            "type": "string",
            "required": "true",
            "description": "recipe id"
        },
        {
              "name": "fields",
              "in": "query",
              "type": "string",
              "description": "fields needed in response separated by comma. e.g: id,name,cook_time"

          }
    ],

    "definitions": DEFINITIONS,

    "responses": {
        "200": {
            "description": "Recipe with its ingredients",
            "schema": {"$ref": "#/definitions/RecipeByIdIngredient"}
        },
        "500": ERROR_RESPONSE
        }
    }

recipe_by_id_ingredient_put = {
    "description": "endpoint to add ingredient to recipe",
    "consumes": ['application/json'],

    "parameters": [
        {
            "name": "recipe_id",
            "in": "path",
            "type": "string",
            "required": "true",
            "description": "recipe id"
        },
        {
            "name": "body",
            "in": "body",
            "required": "true",
            "description": "new data of ingredient for update (all fields are optional)",
            "type": "array",
            "items": {"$ref": "#/definitions/RecipeIngredientPut"}
        },
    ],

    "definitions": DEFINITIONS,

    "responses": {
        "200": {
          "description": "the ingredient updated",
          "schema": {"$ref": "#/definitions/Ingredient"},
        },
        "400": ERROR_RESPONSE,
        "500": ERROR_RESPONSE
      }
}

recipe_by_id_ingredient_delete = {
    "description": "endpoint that deletes all ingredients associated in recipe",
    "parameters": [
        {
            "name": "recipe_id",
            "in": "path",
            "type": "string",
            "required": "true",
            "description": "recipe id"
        }
    ],
    "definitions": DEFINITIONS,
    "responses": {
        "204": {
          "description": "Empty body response",
        },
        "500": ERROR_RESPONSE
      }
}

recipe_by_id_ingredient_by_id_delete = {
    "description": "endpoint that deletes specific ingredient associated to recipe",
    "parameters": [
        {
            "name": "recipe_id",
            "in": "path",
            "type": "string",
            "required": "true",
            "description": "recipe id"
        },
        {
            "name": "ingredient_id",
            "in": "path",
            "type": "integer",
            "required": "true",
            "description": "ingredient id"
        }
    ],
    "definitions": DEFINITIONS,
    "responses": {
        "204": {
          "description": "empty body response",
        },
        "500": ERROR_RESPONSE
      }
}

spec_dict = {
    'recipe_by_id_ingredient': {
      'get': recipe_by_id_ingredient_get,
      'put': recipe_by_id_ingredient_put,
      'delete': recipe_by_id_ingredient_delete
    },
    'recipe_by_id_ingredient_by_id': {
        'delete': recipe_by_id_ingredient_by_id_delete
    }
}