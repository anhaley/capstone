import pandas as pd
import numpy as np
import Connection as c
import os, sys, time
from openpyxl import load_workbook


filename = 'files/Lists.xlsx'
test_table = 'test'
metadata_table = 'metadata'
is_connect = 0
wait_time = 0


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


def get_table(table_name):
    """
    Return a JSON-like format of table data.
    Args:
        table_name: the table to fetch
    Returns: an object-notated dump of the table
    """
    result = []
    column_name = []
    pgSqlCur.execute(f"select * from {table_name}")
    rows = pgSqlCur.fetchall()
    
    for col in pgSqlCur.description:
        column_name.append(col.name)
    
    for row in rows:
        a_row = {}
        i = 0
        for col in column_name:
            a_row[col] = row[i]
            i += 1
        result.append(a_row)

    return result


def read_metadata(filename):
    data = {}
    file_data = load_workbook(filename).properties.__dict__
    os_data = os.stat(filename)
    
    data['filename'] = fmt(os.path.basename(filename))
    data['creator'] = fmt(file_data['creator'])
    data['size'] = os_data.st_size
    data['created'] = fmt(file_data['created'].strftime('%Y-%m-%d %H:%M:%S+08'))
    data['modified'] = fmt(file_data['modified'].strftime('%Y-%m-%d %H:%M:%S+08'))
    data['lastModifiedBy'] = fmt(file_data['lastModifiedBy'])
    data['title'] = fmt(file_data['title'])

    return data


def load_spreadsheet(filename):
    # Read the spreadsheet file into a dataframe object
    return pd.read_excel(filename)


def write_info_data(df):
    """
    Write data from Excel to the information table
    """
    cmd = "INSERT INTO {}(id, firstname, lastname, city) VALUES({}, {}, {}, {}) ON CONFLICT DO NOTHING"
    # unclear what we want to do on collision; depends on data we're inserting

    # potential missing functionality is ability to create a table from a spreadsheet with a non-pre-existing schema
    for i in np.ndenumerate(df.values).iter.base:
        id_, firstname, lastname, city = i
        cf = cmd.format(test_table, id_, fmt(firstname), fmt(lastname), fmt(city))
        print(cf)
        pgSqlCur.execute(cf)


def write_metadata(metadata):
    """
    Write metadata of Excel file into metadata table
    """
    cmd = "INSERT INTO {}(filename, creator, size, created_date, last_modified_date, last_modified_by, title) " \
        "VALUES({},{},{},{},{},{},{}) ON CONFLICT DO NOTHING"
    pgSqlCur.execute(cmd.format(metadata_table, metadata['filename'], metadata['creator'], metadata['size'], metadata['created'],  metadata['modified'],metadata['lastModifiedBy'], metadata['title']))


def process_file(filename):
    """
    Read an Excel file; put info data into info table, metadata into metadata table
    """
    # read file content
    df = load_spreadsheet(filename)
    
    # Write the data to the DB
    write_info_data(df)

    # insert metadata into metadata table
    # should add version and revision to this schema, but don't know types yet
    metadata = read_metadata(filename)
    
    write_metadata(metadata)

    # commit execution
    pgSqlConn.commit()


def db_disconnect():
    c.pgSqlDisconnect(pgSqlCur, pgSqlConn)


def test_driver():
    # Pre-insert query
    print('Dump tables -------------------------------------------------')
    dump_tables()

    print('\nInsert data -------------------------------------------------')
    #populate_file(filename)

    # three options for collisions:
    # 1. do nothing (discard new row; probably want to return an error to the user in this case)
    # 2. update existing record with new metadata
    # ON CONFLICT (filename)
    #       DO UPDATE
    #       SET (size, last_modified_by, modified) = (EXCLUDED.size, EXCLUDED.last_modified_by, EXCLUDED.modified)
    # 3. add entirely new record
    # would need to return status of insertion, then insert a new row. Would need an incrementing column, like 'version'

    # unfortunately, it looks like 'creator' and 'created' are both fabricated by openpyxl, so we may need to find
    # a different way to capture that data if we want to keep them

    # Post insert query, verify data is inserted
    print('\nDump tables -------------------------------------------------')
    dump_tables()

    # close the db connection
    db_disconnect()


# test_driver()
# print(get_table('test'))
if __name__ == '__main__':
    while not is_connect:
        try:
            pgSqlCur, pgSqlConn = c.pgSQLconnect()
            is_connect = 1
        except:
            time.sleep(1)
            wait_time += 1
            sys.stdout.write(f'\rConnecting to DB ... {wait_time}')