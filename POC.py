
import pandas as pd
import Connection as c
import sqlalchemy as sql

# Read in the excel file into a dataframe object
df = pd.read_excel('Lists.xlsx')
df.head()
print(df)

pgSQLconn = None
# create the postgresql cursor and connection
pgSQLcur, pgSQLconn = c.pgSQLconnect()

#create connection for panda.to_sql to write to DB
engine = sql.create_engine("postgresql://seanmitchell:@localhost/seanmitchell")

# Pre insert query
pgSQLcur.execute("select * from test")
row = pgSQLcur.fetchall()
for rows in row:
    print(rows)

# Write the dataframe to the DB
df.to_sql('test', con=engine,if_exists='append')

# Post insert query to very data is inserted
pgSQLcur.execute("select * from test")
row = pgSQLcur.fetchall()
for rows in row:
    print(rows)

# close the db connection
c.pgSQLdisconnect(pgSQLcur,pgSQLconn)

