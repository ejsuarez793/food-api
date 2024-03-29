CREATE TABLE recipe (
    id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    veggie_friendly BOOLEAN NOT NULL,
    meal_type VARCHAR[] NOT NULL,
    cook_time INTEGER NOT NULL,
    wash_time INTEGER NOT NULL,
    cook_technique VARCHAR NOT NULL,
    info JSON NOT NULL,
    steps JSON NOT NULL,
	date_created TIMESTAMP NOT NULL,
	last_updated TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);