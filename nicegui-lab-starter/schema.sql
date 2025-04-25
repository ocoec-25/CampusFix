DROP TABLE IF EXISTS enroll;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;

CREATE TABLE students (
    student_id INT PRIMARY KEY NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    grad_year INT NOT NULL
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY NOT NULL,
    department VARCHAR(10) NOT NULL,
    course_number INT NOT NULL,
    course_section INT NOT NULL,
    course_name VARCHAR(50) NOT NULL,
    start_time TIME NOT NULL,
    prof_name VARCHAR(50)
);

CREATE TABLE enroll (
    student_id INT REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    PRIMARY KEY (student_id, course_id)
);
