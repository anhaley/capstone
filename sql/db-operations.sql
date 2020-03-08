/*
A file record some DB operation that may use in the program

*/


-- dump table
select * from test;
select * from metadata;

-- insert rows
INSERT INTO test(id, firstname, lastname) VALUES(1, 'a', 'b') ON CONFLICT DO NOTHING;


-- clear table
DELETE FROM test;


