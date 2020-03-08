#!/usr/bin/python
import sys
import psycopg2
from dbConfig import pgSqlConfig



def pgSQLconnect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = pgSqlConfig()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        conn.commit()
        return cur, conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def pgSqlDisconnect(cur, conn):
    try:
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')