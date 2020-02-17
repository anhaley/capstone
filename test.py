#!/usr/bin/python
import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=capstone")
cur = conn.cursor()

f = open('example.csv', 'r')

cur.execute("Truncate {} Cascade;".format('capstone'))
cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format('capstone'), f)
cur.execute("commit;")

conn.close()
f.close()
