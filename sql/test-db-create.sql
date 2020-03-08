

CREATE TABLE test (
    id 			INTEGER  PRIMARY KEY,
    firstname 	TEXT NOT NULL,
    lastname 	TEXT NOT NULL
);

CREATE TABLE metadata (
    filename TEXT NOT NULL,
    creator TEXT NOT NULL,
    size INT,
    created_date TIMESTAMP,
    last_modified_date TIMESTAMP,
    last_modified_by TEXT,
    title TEXT
);

