/*
A file to record some DB operation for later reference
that may use in the program

*/


-- dump table
select * from test;
select * from metadata;

-- insert rows
INSERT INTO test(id, firstname, lastname, city) VALUES(1, 'a', 'b', 'c') ON CONFLICT DO NOTHING;


-- clear table
DELETE FROM test;

-- delete table
drop table test;
