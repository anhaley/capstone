import csv
import psycopg2

#code more or less taken from: https://stackoverflow.com/questions/3710263/how-do-i-create-a-csv-file-from-database-in-python
from glob import glob; from os.path import expanduser
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=pass")
cursor = conn.cursor()
cursor.execute("select * from capstone;") 
with open("out.csv", "wb") as csv_file:              # Python 2 version
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description]) # write headers
    csv_writer.writerows(cursor)
