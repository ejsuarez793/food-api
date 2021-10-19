from app.swagger import DEFINITIONS, SEARCH_PARAMETERS, ERROR_RESPONSE

recipe_get = {
    "description": "endpoint for making recipes multiget, and ingredient searchs (filters, sorting and pagination available)",
    "parameters": SEARCH_PARAMETERS,

    "definitions": DEFINITIONS,

    "responses": {
        "200": {
            "description": "recipes list of search results (fields may be filtered)",
            "type": "array",
            "schema": {"$ref": "#/definitions/RecipeSearch"}
        },
        "500": ERROR_RESPONSE
        }
    }

recipe_post = {
    "description": "endpoint for recipe creation",
    "consumes": ['application/json'],

    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": "true",
            "description": "recipe data",
            "type": "object",
            "schema": {"$ref": "#/definitions/Recipe"}
        },
    ],

    "definitions": DEFINITIONS,

    "responses": {
        "200": {
          "description": "the recipe newly created",
          "schema": {"$ref": "#/definitions/Recipe"},
        },
        "400": ERROR_RESPONSE,
        "500": ERROR_RESPONSE
      }
}

recipe_by_id_get = {
    "description": "endpoint to retrieve recipe by id",
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
          "description": "The recipe (fields may be filtered)",
          "schema": {"$ref": "#/definitions/Recipe"},
        },
        "404": ERROR_RESPONSE,
        "500": ERROR_RESPONSE
      }
}

recipe_by_id_put = {
    "description": "endpoint to update recipe",
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
            "description": "new data of recipe for update (some fields are optional)",
            "type": "object",
            "schema": {"$ref": "#/definitions/Recipe"}
        },
    ],

    "definitions": DEFINITIONS,

    "responses": {
        "200": {
          "description": "The recipe updated",
          "schema": {"$ref": "#/definitions/Recipe"},
        },
        "404": ERROR_RESPONSE,
        "500": ERROR_RESPONSE
      }
}

recipe_by_id_delete = {
    "description": "endpoint to delete recipe",
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


spec_dict = {
  'recipe': {
      'get': recipe_get,
      'post': recipe_post
  },
  'recipe_by_id': {
    'get': recipe_by_id_get,
    'delete': recipe_by_id_delete,
    'put': recipe_by_id_put
  }
}