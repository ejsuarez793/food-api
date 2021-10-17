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

recipe_by_id_get = {
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
        "Recipe": RECIPE,
        "ErrorMsg": ERROR_MSG
      },

      "responses": {
        "200": {
          "description": "The recipe (fields may be filtered)",
          "schema": {"$ref": "#/definitions/Recipe"},
        },
        "404": {
          "description": "Not found message",
          "schema": {"$ref": "#/definitions/ErrorMsg"}
        },
        "500": {
          "description": "Server error message",
          "schema": {"$ref": "#/definitions/ErrorMsg"}
        }
      }
}

recipe_by_id_put = {
    "consumes": ['application/json'],

    "parameters": [{
      "name": "id",
      "in": "path",
      "type": "string",
      "required": "true",
        "description": "recipe id"
    },
    {
            "name": "body",
            "in": "body",
            "required": "true",
            "description": "new data of recipe for update (some fields are optional)",
            "type": "object",
            "schema": {"$ref": "#/definitions/Recipe"}
        },
    ],

    "definitions": {
        "Recipe": RECIPE,
        "ErrorMsg": ERROR_MSG
      },

    "responses": {
        "200": {
          "description": "The recipe updated",
          "schema": {"$ref": "#/definitions/Recipe"},
        },
        "404": {
          "description": "Not found message",
          "schema": {"$ref": "#/definitions/ErrorMsg"}
        },
        "500": {
          "description": "Server error message",
          "schema": {"$ref": "#/definitions/ErrorMsg"}
        }
      }
}

recipe_by_id_delete = {
    "parameters": [{
      "name": "id",
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


spec_dict = {
  'recipe': {},
  'recipe_by_id': {
    'get': recipe_by_id_get,
    'delete': recipe_by_id_delete,
    'put': recipe_by_id_put
  }
}