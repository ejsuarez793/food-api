-- ToDo: revisar naming convention para las tablas (singular en vez de plural, recipe en vez de recipes)

CREATE TABLE recipe_ingredient (
    recipe_id       varchar REFERENCES recipes (id) ON UPDATE CASCADE ON DELETE CASCADE,
    ingredient_id   bigint  REFERENCES ingredients (id) ON UPDATE CASCADE ON DELETE CASCADE,
    amount          numeric (1000, 4) NOT NULL,
    measure_unit    varchar NOT NULL,

    CONSTRAINT recipe_ingredient_pkey PRIMARY KEY (recipe_id, ingredient_id)
);