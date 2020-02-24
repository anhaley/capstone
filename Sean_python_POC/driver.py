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
df = pd.read_excel(filename)
metadata = load_workbook(filename).properties.__dict__
os_data = os.stat(filename)
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
# cmd = text("""INSERT INTO test(id, firstname, lastname) VALUES(:id, :firstname, :lastname) ON CONFLICT DO NOTHING""")
cmd = "INSERT INTO test(id, firstname, lastname) VALUES({}, {}, {}) ON CONFLICT DO NOTHING"

# fix this so index is properly accounted for
# revision, version, creator, lastModifiedBy, modified, created, title, subject, description, identifier, keywords

r = dict()
for i in np.ndenumerate(df.values).iter.base:
    r['id'], r['firstname'], r['lastname'] = i
    cf = cmd.format(r['id'], "'"+r['firstname']+"'", "'"+r['lastname']+"'")
    print(cf)
    pgSqlCur.execute(cf)

# insert metadata into metadata table

pgSqlConn.commit()

# Post insert query, verify data is inserted
pgSqlCur.execute("select * from test")
row = pgSqlCur.fetchall()
for rows in row:
    print(rows)

for key in metadata:
    print(key, ': ', metadata[key])
metadata['size'] = os_data.st_size

# close the db connection
c.pgSqlDisconnect(pgSqlCur, pgSqlConn)

