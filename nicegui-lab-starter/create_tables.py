import psycopg
from dbinfo import *
from psycopg.rows import dict_row

def main():
    # Connect to an existing database
    conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    file = open("schema.sql", "r")  # open the file
    alltext = file.read()  # read all the text
    cur.execute(alltext)  # execute all the SQL in the file
    conn.commit()  # Actually make the changes to the db

    cur.close()
    conn.close()

main()