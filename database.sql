DROP TABLE IF EXISTS urls;


CREATE TABLE urls (
    id bigint GENERATED ALWAYS AS IDENTITY,
    name varchar(255) NOT NULL,
    created_at TIMESTAMP
    );
