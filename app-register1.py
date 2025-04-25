# Script to let us register students.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def get_students():
    cur.execute("SELECT student_id, first_name, last_name, grad_year FROM students")
    rows = cur.fetchall()
    return rows

def get_classes_for_student(student_id):
    cur.execute("SELECT * from enroll NATURAL JOIN courses WHERE student_id=%s", [student_id])
    rows = cur.fetchall()
    return rows

@ui.page('/')
def homepage():
    ui.label("Welcome to the homepage!")
    ui.link("Register for classes", '/register')

@ui.page('/register')
def register():
    with ui.card() as step1_card:
        with ui.row().classes('items-center'):
            ui.label('Student ID:')
            student_id_box = ui.input()
        ui.button('Get Schedule', on_click=lambda: process_step1())

    with ui.card() as step2_card:
        ui.label("Student Schedule:")
        cols = [{'name': 'course_id', 'field': 'course_id', 'label': "Course ID"},
                {'name': 'department', 'field': 'department', 'label': "Dept"},
                {'name': 'course_number', 'field': 'course_number', 'label': "Course Num"},
                {'name': 'course_section', 'field': 'course_section', 'label': "Section"},
                {'name': 'start_time', 'field': 'start_time', 'label': "Time"}]
        my_classes_table = ui.table(columns=cols, rows=[])

        ui.label("Classes available:")
        avail_classes_table = ui.table(columns=cols, rows=[])

        ui.button('Register!', on_click=lambda: process_step2())
    step2_card.set_visibility(False)

    def process_step1():
        print(student_id_box.value)
        schedule_rows = get_classes_for_student(student_id_box.value)
        print(schedule_rows)
        step1_card.set_visibility(False)
        my_classes_table.add_rows(schedule_rows)
        my_classes_table.update()

        # Add code to add classes to avail_classes_table

        step2_card.set_visibility(True)

    def process_step2():
        # Add code to register the student for the class
        pass


ui.run(reload=False)
