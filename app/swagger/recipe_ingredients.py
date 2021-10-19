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

recipe_by_id_ingredient_get = {
    "description": "endpoint to retrieve recipe and its ingredients by recipe id",
    "parameters": [
        {
            "name": "id",
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

    "definitions": {
        "RecipeByIdIngredient": RECIPE_BY_ID,
        "ErrorMsg": ERROR_MSG,
        "RecipeIngredient": RECIPE_INGREDIENT
    },

    "responses": {
        "200": {
            "description": "Recipe with its ingredients",
            "schema": {"$ref": "#/definitions/RecipeByIdIngredient"}
        },
        "500": {
              "description": "Server error message",
              "schema": {"$ref": "#/definitions/ErrorMsg"}
            }
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

    "definitions": {
        "RecipeIngredientPut": RECIPE_INGREDIENT_PUT,
        "ErrorMsg": ERROR_MSG
    },

    "responses": {
        "200": {
          "description": "the ingredient updated",
          "schema": {"$ref": "#/definitions/Ingredient"},
        },
        "400": {
          "description": "validation error message",
          "schema": {"$ref": "#/definitions/ErrorMsg"}
        },
        "500": {
          "description": "server error message",
          "schema": {"$ref": "#/definitions/ErrorMsg"}
        }
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
    "definitions": {
      "ErrorMsg": ERROR_MSG
    },
    "responses": {
        "204": {
          "description": "Empty body response",
        },
        "500": {
          "description": "Server error message",
          "schema": {"$ref": "#/definitions/ErrorMsg"}
        }
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
    "definitions": {
      "ErrorMsg": ERROR_MSG
    },
    "responses": {
        "204": {
          "description": "empty body response",
        },
        "500": {
          "description": "server error message",
          "schema": {"$ref": "#/definitions/ErrorMsg"}
        }
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