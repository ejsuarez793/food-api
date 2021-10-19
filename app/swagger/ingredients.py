from app.swagger import DEFINITIONS, SEARCH_PARAMETERS, ERROR_RESPONSE

ingredient_get = {
    "description": "endpoint for making ingredients multiget, and ingredient searchs (filters, sorting and pagination available)",
    "parameters": SEARCH_PARAMETERS,

    "definitions": DEFINITIONS,

    "responses": {
        "200": {
            "description": "ingredient list of search results (fields may be filtered)",
            "type": "array",
            "schema": {"$ref": "#/definitions/IngredientSearch"}
        },
        "500": ERROR_RESPONSE
        }
    }

ingredient_post = {
    "description": "endpoint for ingredient creation",
    "consumes": ['application/json'],

    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": "true",
            "description": "ingredient data",
            "type": "object",
            "schema": {"$ref": "#/definitions/Ingredient"}
        },
    ],

    "definitions": DEFINITIONS,

    "responses": {
        "200": {
          "description": "the ingredient newly created",
          "schema": {"$ref": "#/definitions/Ingredient"},
        },
        "400": ERROR_RESPONSE,
        "500": ERROR_RESPONSE,
      }
}

ingredient_by_id_get = {
    "description": "endpoint to retrieve ingredient by id",
      "parameters": [
          {
            "name": "ingredient_id",
            "in": "path",
            "type": "integer",
            "required": "true",
            "description": "ingredient id"
          },
          {
              "name": "fields",
              "in": "query",
              "type": "string",
              "description": "fields needed in response separated by comma. e.g: id,name,storage"

          }
      ],

      "definitions": DEFINITIONS,

      "responses": {
        "200": {
          "description": "The ingredient (fields may be filtered)",
          "schema": {"$ref": "#/definitions/Ingredient"},
        },
        "404": ERROR_RESPONSE,
        "500": ERROR_RESPONSE
      }
}


ingredient_by_id_put = {
    "description": "endpoint to update ingredient data",
    "consumes": ['application/json'],

    "parameters": [
        {
            "name": "ingredient_id",
            "in": "path",
            "type": "string",
            "required": "true",
            "description": "ingredient id"
        },
        {
            "name": "body",
            "in": "body",
            "required": "true",
            "description": "new data of ingredient for update (all fields are optional)",
            "type": "object",
            "schema": {"$ref": "#/definitions/Ingredient"}
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


ingredient_by_id_delete = {
    "description": "endpoint to delete ingredient",
    "parameters": [
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
          "description": "Empty body response",
        },
        "500": ERROR_RESPONSE
      }
}

spec_dict = {
  'ingredient': {
      'get': ingredient_get,
      'post': ingredient_post
  },
  'ingredient_by_id': {
    'get': ingredient_by_id_get,
    'put': ingredient_by_id_put,
    'delete': ingredient_by_id_delete
  }
}