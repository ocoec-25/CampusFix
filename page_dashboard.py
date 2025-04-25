
import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui, app

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def get_courses_by_enrollment():
    cur.execute("WITH enrollments AS (SELECT course_id, count(*) as num_enrolled FROM enroll GROUP BY course_id) " +
        "SELECT course_id, department, course_number, course_section, num_enrolled FROM enrollments NATURAL JOIN courses " +
        "ORDER BY num_enrolled DESC")
    rows = cur.fetchall()
    return rows

@ui.page('/dashboard')
def dashboard():
    # Queries:
    # Top classes by enrollment - show as histogram, break down by individual course (id) and by course number
    # Breakdown of classes by time of day - show as a pie chart
    # Students by graduation year - show as a histogram (bar chart)
    # BONUS: for top classes by enrollment, add checkboxes for graduation year, only show students in checked grad year boxes.
    #   see https://nicegui.io/documentation/echart for how to automatically update a chart based on a click

    ui.markdown("# Super cool dashboard!")

    class_data = get_courses_by_enrollment()
    print(class_data)

    class_names = [row['department'] + str(row['course_number']) + "-" + str(row["course_section"]) for row in class_data]
    student_counts = [row['num_enrolled'] for row in class_data]

    ui.echart({
        'title': {'text': 'Class Enrollment'},
        'tooltip': {'trigger': 'axis'},
        'xAxis': {
            'type': 'category',
            'data': class_names,
            'axisLabel': {'interval': 0, 'rotate': 30},  # helpful if labels are long
        },
        'yAxis': {
            'type': 'value',
            'name': 'Number of Students',
        },
        'series': [{
            'data': student_counts,
            'type': 'bar',
            'name': 'Students',
            'itemStyle': {
                'color': '#3398DB'
            }
        }]
    })

    class_data = [
        {'class_name': 'CS101', 'students': 35},
        {'class_name': 'MATH202', 'students': 28},
        {'class_name': 'ENG150', 'students': 22},
        {'class_name': 'BIO110', 'students': 40},
    ]

    pie_data = [{'name': row['class_name'], 'value': row['students']} for row in class_data]

    ui.echart({
        'title': {
            'text': 'Students per Class',
            'left': 'center'
        },
        'tooltip': {
            'trigger': 'item'
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left'
        },
        'series': [{
            'name': 'Class',
            'type': 'pie',
            'radius': '50%',
            'data': pie_data,
            'emphasis': {
                'itemStyle': {
                    'shadowBlur': 10,
                    'shadowOffsetX': 0,
                    'shadowColor': 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    })



