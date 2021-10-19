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

recipe_get = {
    "description": "endpoint for making recipes multiget, and ingredient searchs (filters, sorting and pagination available)",
    "parameters": [
        {
            "name": "ids",
            "in": "query",
            "type": "str",
            "description": "ids of the recipes to search separated by comma (max ids is 20). if set all other parameters are ignored",
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
    ],

    "definitions": {
        "Ingredient": RECIPE,
        "ErrorMsg": ERROR_MSG,
        "Pagination": PAGINATION,
        "RecipeSearch": RECIPE_SEARCH
    },

    "responses": {
        "200": {
            "description": "recipes list of search results (fields may be filtered)",
            "type": "array",
            "schema": {"$ref": "#/definitions/RecipeSearch"}
        },
        "500": {
              "description": "server error message",
              "schema": {"$ref": "#/definitions/ErrorMsg"}
            }
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

    "definitions": {
        "Ingredient": RECIPE,
        "ErrorMsg": ERROR_MSG
    },

    "responses": {
        "200": {
          "description": "the recipe newly created",
          "schema": {"$ref": "#/definitions/Recipe"},
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

recipe_by_id_get = {
    "description": "endpoint to retrieve recipe by id",
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
    "description": "endpoint to update recipe",
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
    "description": "endpoint to delete recipe",
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