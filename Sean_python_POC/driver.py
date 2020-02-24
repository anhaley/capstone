import xlrd
import pandas as pd
from sqlalchemy import text
import numpy as np

import Connection as c
import sqlalchemy as sql
import os
from openpyxl import load_workbook

# Read in the excel file into a dataframe object
filename = 'Lists.xlsx'
db = 'test'
metadata_db = 'metadata'
df = pd.read_excel(filename)
df.head()

# create the postgresql cursor and connection
pgSqlCur, pgSqlConn = c.pgSQLconnect()

#create connection for panda.to_sql to write to DB
engine = sql.create_engine("postgresql+psycopg2://andrew:password@localhost:5432/test")

# Pre insert query
pgSqlCur.execute("select * from test")
row = pgSqlCur.fetchall()
for rows in row:
    print(rows)

# Write the dataframe to the DB
cmd = "INSERT INTO {}(id, firstname, lastname) VALUES({}, {}, {}) ON CONFLICT DO NOTHING"

r = dict()
for i in np.ndenumerate(df.values).iter.base:
    r['id'], r['firstname'], r['lastname'] = i
    cf = cmd.format(db, r['id'], "'"+r['firstname']+"'", "'"+r['lastname']+"'")
    print(cf)
    pgSqlCur.execute(cf)

# potential missing functionality is ability to create a table from a spreadsheet with a non-pre-existing schema

# insert metadata into metadata table
# filename, creator, size, version, revision, created, modified, lastModifiedBy, title, subject, description
# create table metadata(filename varchar(200), creator varchar(100), size int, last_modified_by varchar(200), created timestamp, modified timestamp, title varchar(200));
# should add version and revision to this schema, but don't know types yet
metadata = load_workbook(filename).properties.__dict__
os_data = os.stat(filename)
cmd = "INSERT INTO {}(filename, creator, size, last_modified_by, created, modified, title) VALUES({},{},{},{},{},{},{})"
metadata['size'] = os_data.st_size

# datetime read/write conflict. need to parse into something Python can handle, then write into something PG-friendly

pgSqlCur.execute(cmd.format(metadata_db, filename, metadata['creator'], metadata['size'], metadata['lastModifiedBy'],
                            metadata['created'], metadata['modified'], metadata['title']))

pgSqlConn.commit()

# Post insert query, verify data is inserted
pgSqlCur.execute("select * from test")
rows = pgSqlCur.fetchall()
for row in rows:
    print(row)


# close the db connection
c.pgSqlDisconnect(pgSqlCur, pgSqlConn)

