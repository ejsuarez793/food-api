CREATE TABLE ingredient (
	id SERIAL,
    name VARCHAR NOT NULL,
    food_group VARCHAR NOT NULL,
    veggie_friendly BOOLEAN NOT NULL,
    storage VARCHAR NOT NULL,
    expiration_time INTERVAL NOT NULL,
    date_created TIMESTAMP NOT NULL,
    last_updated TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);