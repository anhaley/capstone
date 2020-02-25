import pandas as pd
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

# create connection for panda.to_sql to write to DB
engine = sql.create_engine("postgresql+psycopg2://andrew:password@localhost:5432/test")


def fmt(s):
    if s is None:
        s = "NULL"
    else:
        s = "'" + str(s) + "'"
    return s


def dump_tables():
    print("Test:\n-------------------------------")
    pgSqlCur.execute("select * from test")
    rows = pgSqlCur.fetchall()
    for row in rows:
        print(row)
    print("\nMetadata:\n-------------------------------")
    pgSqlCur.execute("select * from metadata")
    rows = pgSqlCur.fetchall()
    for row in rows:
        print(row)


# Pre-insert query
dump_tables()

# Write the dataframe to the DB
cmd = "INSERT INTO {}(id, firstname, lastname) VALUES({}, {}, {}) ON CONFLICT DO NOTHING"

# potential missing functionality is ability to create a table from a spreadsheet with a non-pre-existing schema
for i in np.ndenumerate(df.values).iter.base:
    id_, firstname, lastname = i
    cf = cmd.format(db, id_, fmt(firstname), fmt(lastname))
    print(cf)
    pgSqlCur.execute(cf)


# insert metadata into metadata table
# should add version and revision to this schema, but don't know types yet
metadata = load_workbook(filename).properties.__dict__
os_data = os.stat(filename)
metadata['size'] = os_data.st_size
for item in metadata:
    metadata[item] = fmt(metadata[item])

cmd = "INSERT INTO {}(filename, creator, size, last_modified_by, created, modified, title) " \
      "VALUES({},{},{},{},{},{},{}) ON CONFLICT DO NOTHING"
# TODO: change DO NOTHING to an update by either adding a COPY field or erasing the previous record

pgSqlCur.execute(cmd.format(metadata_db, fmt(filename), metadata['creator'], metadata['size'], metadata['lastModifiedBy'],
                            metadata['created'], metadata['modified'], metadata['title']))

pgSqlConn.commit()

# Post insert query, verify data is inserted
dump_tables()

# close the db connection
c.pgSqlDisconnect(pgSqlCur, pgSqlConn)

