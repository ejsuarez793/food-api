CREATE TABLE recipe_ingredient (
    recipe_id       varchar REFERENCES recipe (id) ON UPDATE CASCADE ON DELETE CASCADE,
    ingredient_id   bigint  REFERENCES ingredient (id) ON UPDATE CASCADE ON DELETE CASCADE,
    amount          numeric (1000, 4) NOT NULL,
    measure_unit    varchar NOT NULL,
    optional BOOLEAN  NOT NULL,

    CONSTRAINT recipe_ingredient_pkey PRIMARY KEY (recipe_id, ingredient_id)
);