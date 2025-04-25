# Script to let us register students.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui, app

from page_protected import protected
from page_dashboard import dashboard

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

def get_non_conflicting_classes_for_student(student_id):
    cur.execute("SELECT * from courses where start_time" +
                " not in (SELECT start_time FROM enroll NATURAL JOIN courses WHERE student_id=%s)", [student_id])
    rows = cur.fetchall()
    return rows

# pretend graduation year is the user's password
def get_password_for_user(student_id):
    cur.execute("SELECT grad_year from students where student_id=%s", [student_id])
    row = cur.fetchone()
    return str(row['grad_year'])  # return as a string to simulate a password

@ui.page('/')
def homepage():
    ui.label("Welcome to the homepage!")

    username = app.storage.user.get('username', None)   # default if not logged in is None
    if username is not None:
        ui.label("You are logged in as user: " + username)
    else:
        ui.label("You are not logged in.")

    ui.link("Login", '/login')
    ui.link("Logout", '/logout')
    ui.link("Register for classes", '/register')
    ui.link("Drop a class", '/drop')
    ui.link("Password-protected test page", '/protected')
    ui.link("Dashboard", '/dashboard')


@ui.page('/login')
def login(redirect_url = '/'):
    def try_login():
        password = get_password_for_user(username_box.value)
        if password == password_box.value:
            app.storage.user['username'] = username_box.value
            ui.navigate.to(redirect_url)  # go to where the user wanted to go
        else:
            ui.notify('Wrong username or password', color='negative')

    #if app.storage.user.get('authenticated', False):
    #        return RedirectResponse('/')
    ui.label("Use a user_id number for username and the grad year for password.")
    with ui.row().classes('items-center'):
        username_box = ui.input('Username:')
        password_box = ui.input('Password', password=True, password_toggle_button=True)
        ui.button('Log in', on_click=try_login)

@ui.page('/logout')
def logout():
    app.storage.user.pop('username')
    ui.label("You are now logged out.")
    ui.link("Back to homepage", '/')

@ui.page('/register')
def register():
    selected_student = None
    selected_class = None
    with ui.card() as step1_card:
        ui.label("Available students: ")
        student_rows = get_students()
        students_table = ui.table(rows=student_rows, selection='single', row_key='student_id',
                                  on_select=lambda e: click_student(e))
        ui.button('Get Schedule', on_click=lambda: process_step1())

    with ui.card() as step2_card:
        ui.label("Student Schedule:")
        cols = [{'name': 'course_id', 'field': 'course_id', 'label': "Course ID"},
                {'name': 'department', 'field': 'department', 'label': "Dept"},
                {'name': 'course_number', 'field': 'course_number', 'label': "Course Num"},
                {'name': 'course_section', 'field': 'course_section', 'label': "Section"},
                {'name': 'start_time', 'field': 'start_time', 'label': "Time"}]
        my_classes_table = ui.table(columns=cols, rows=[])

        ui.label("Classes available (non conflicting):")
        avail_classes_table = ui.table(columns=cols, rows=[],
                                       selection='single', row_key='course_id',
                                       on_select=lambda e: click_class(e))

        ui.button('Register!', on_click=lambda: process_step2())

    with ui.card() as step3_card:
        ui.label("New Schedule:")
        cols = [{'name': 'course_id', 'field': 'course_id', 'label': "Course ID"},
                {'name': 'department', 'field': 'department', 'label': "Dept"},
                {'name': 'course_number', 'field': 'course_number', 'label': "Course Num"},
                {'name': 'course_section', 'field': 'course_section', 'label': "Section"},
                {'name': 'start_time', 'field': 'start_time', 'label': "Time"}]
        my_new_classes_table = ui.table(columns=cols, rows=[])

    step2_card.set_visibility(False)
    step3_card.set_visibility(False)

    def click_student(e):
        nonlocal selected_student
        print(e.selection)
        selected_student = e.selection[0]['student_id']

    def click_class(e):
        nonlocal selected_class
        print(e.selection)
        selected_class = e.selection[0]['course_id']

    def process_step1():
        schedule_rows = get_classes_for_student(selected_student)
        print(schedule_rows)
        step1_card.set_visibility(False)
        my_classes_table.add_rows(schedule_rows)
        my_classes_table.update()

        # Add code to add classes to avail_classes_table
        non_conflicting_classes = get_non_conflicting_classes_for_student(selected_student)
        avail_classes_table.add_rows(non_conflicting_classes)

        step2_card.set_visibility(True)

    def process_step2():
        # Add code to register the student for the class
        print(selected_class)
        cur.execute("INSERT INTO enroll (student_id, course_id) VALUES (%s, %s)", [selected_student, selected_class])
        conn.commit()

        # get the updated schedule
        schedule_rows = get_classes_for_student(selected_student)
        my_new_classes_table.add_rows(schedule_rows)
        my_new_classes_table.update()

        step2_card.set_visibility(False)
        step3_card.set_visibility(True)

@ui.page('/drop')
def drop():
    selected_student = None
    selected_class = None
    with ui.card() as step1_card:
        ui.label("Available students: ")
        student_rows = get_students()
        students_table = ui.table(rows=student_rows, selection='single', row_key='student_id',
                                  on_select=lambda e: click_student(e))
        ui.button('Get Schedule', on_click=lambda: process_step1())

    with ui.card() as step2_card:
        ui.label("Student Schedule:")
        cols = [{'name': 'course_id', 'field': 'course_id', 'label': "Course ID"},
                {'name': 'department', 'field': 'department', 'label': "Dept"},
                {'name': 'course_number', 'field': 'course_number', 'label': "Course Num"},
                {'name': 'course_section', 'field': 'course_section', 'label': "Section"},
                {'name': 'start_time', 'field': 'start_time', 'label': "Time"}]
        my_classes_table = ui.table(columns=cols, rows=[], selection='single',
                                    row_key='course_id',
                                    on_select=lambda e: click_class(e))

        ui.button('Drop!', on_click=lambda: process_step2())

    with ui.card() as step3_card:
        ui.label("New Schedule:")
        cols = [{'name': 'course_id', 'field': 'course_id', 'label': "Course ID"},
                {'name': 'department', 'field': 'department', 'label': "Dept"},
                {'name': 'course_number', 'field': 'course_number', 'label': "Course Num"},
                {'name': 'course_section', 'field': 'course_section', 'label': "Section"},
                {'name': 'start_time', 'field': 'start_time', 'label': "Time"}]
        my_new_classes_table = ui.table(columns=cols, rows=[])

    step2_card.set_visibility(False)
    step3_card.set_visibility(False)

    def click_student(e):
        nonlocal selected_student
        print(e.selection)
        selected_student = e.selection[0]['student_id']

    def click_class(e):
        nonlocal selected_class
        print(e.selection)
        selected_class = e.selection[0]['course_id']

    def process_step1():
        schedule_rows = get_classes_for_student(selected_student)
        print(schedule_rows)
        step1_card.set_visibility(False)
        my_classes_table.add_rows(schedule_rows)
        my_classes_table.update()

        # Add code to add classes to avail_classes_table
        #non_conflicting_classes = get_non_conflicting_classes_for_student(selected_student)
        #avail_classes_table.add_rows(non_conflicting_classes)

        step2_card.set_visibility(True)

    def process_step2():
        # Add code to register the student for the class
        print(selected_class)
        #cur.execute("INSERT INTO enroll (student_id, course_id) VALUES (%s, %s)", [selected_student, selected_class])
        cur.execute("DELETE FROM enroll WHERE student_id=%s AND course_id=%s", [selected_student, selected_class])
        conn.commit()

        # get the updated schedule
        schedule_rows = get_classes_for_student(selected_student)
        my_new_classes_table.add_rows(schedule_rows)
        my_new_classes_table.update()

        step2_card.set_visibility(False)
        step3_card.set_visibility(True)




ui.run(reload=False, storage_secret='THIS_NEEDS_TO_BE_CHANGED')
