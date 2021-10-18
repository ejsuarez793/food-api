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


ingredient_get = {
    "parameters": [
        {
            "name": "ids",
            "in": "query",
            "type": "str",
            "description": "ids of the ingredient to search separated by comma (max ids is 20). if set all other parameters are ignored",
        },
        {
            "name": "fields",
            "in": "query",
            "type": "string",
            "description": "fields needed in response separated by comma. e.g: id,name,storage"
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
        "Ingredient": INGREDIENT,
        "ErrorMsg": ERROR_MSG,
        "Pagination": PAGINATION,
        "IngredientSearch": INGREDIENT_SEARCH
    },

    "responses": {
        "200": {
            "description": "ingredient list of search results (fields may be filtered)",
            "type": "array",
            "schema": {"$ref": "#/definitions/IngredientSearch"}
        },
        "500": {
              "description": "Server error message",
              "schema": {"$ref": "#/definitions/ErrorMsg"}
            }
        }
    }

ingredient_post = {
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

    "definitions": {
        "Ingredient": INGREDIENT,
        "ErrorMsg": ERROR_MSG
    },

    "responses": {
        "200": {
          "description": "the ingredient newly created",
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

ingredient_by_id_get = {
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

      "definitions": {
        "Ingredient": INGREDIENT,
        "ErrorMsg": ERROR_MSG
      },

      "responses": {
        "200": {
          "description": "The ingredient (fields may be filtered)",
          "schema": {"$ref": "#/definitions/Ingredient"},
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


ingredient_by_id_put = {
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

    "definitions": {
        "Ingredient": INGREDIENT,
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


ingredient_by_id_delete = {
    "parameters": [
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
          "description": "Empty body response",
        },
        "500": {
          "description": "Server error message",
          "schema": {"$ref": "#/definitions/ErrorMsg"}
        }
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