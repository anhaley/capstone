/*
This SQL file will be executed once the DB has set up.
It will contain SQL command to set up required DBs and tables

*/

CREATE TABLE IF NOT EXISTS test  (
    id 			INTEGER  PRIMARY KEY,
    firstname 	TEXT NOT NULL,
    lastname 	TEXT NOT NULL,
    city        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS metadata (
    filename TEXT NOT NULL,
    creator TEXT NOT NULL,
    size INT,
    created_date TIMESTAMP,
    last_modified_date TIMESTAMP,
    last_modified_by TEXT,
    title TEXT
);

