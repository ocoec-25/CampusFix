# Script to let us test the functionality of the courses table.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def list_courses():
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    print("Here are the courses:")
    for course in rows:
        print("ID:", course['course_id'], "Dept:", course['department'], "Number:", course['course_number'])

def add_courses_from_csv(filename):
    with open(filename, 'r') as file:
        with cur.copy(f"COPY courses FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

def delete_all_courses():
    cur.execute("DELETE FROM courses")  # careful! deletes everything.
    conn.commit()

def main():
    list_courses()
    delete_all_courses()
    add_courses_from_csv("courses.csv")
    list_courses()


main()
cur.close()
conn.close()