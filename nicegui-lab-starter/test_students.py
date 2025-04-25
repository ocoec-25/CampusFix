# Script to let us test the functionality of the user table.
# Can add a user, print them, read from CSV.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def list_students():
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    print("Here are the students:")
    for student in rows:
        print("ID:", student['student_id'], "Name:", student['first_name'], student['last_name'])

def add_students_from_csv(filename):
    with open(filename, 'r') as file:
        with cur.copy(f"COPY students FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

def delete_all_students():
    cur.execute("DELETE FROM students")  # careful! deletes everything.
    conn.commit()

def add_student_manually():
    id = int(input("Enter a new student ID: "))
    first = input("Enter first name: ")
    last = input("Enter last name: ")
    year = int(input("Enter graduation year: "))
    cur.execute("INSERT INTO students (student_id, first_name, last_name, grad_year) VALUES (%s, %s, %s, %s)", [id, first, last, year])
    conn.commit()  # mandatory to actually write the data to the db

def main():
    list_students()
    delete_all_students()
    add_students_from_csv("students.csv")
    add_student_manually()
    list_students()


main()
cur.close()
conn.close()