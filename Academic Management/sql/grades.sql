USE student_management;

CREATE TABLE IF NOT EXISTS grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    marks DECIMAL(5,2) NOT NULL,
    grade VARCHAR(2),
    grade_point DECIMAL(3,2),
    semester INT NOT NULL,

    UNIQUE (student_id, course_id, semester),

    FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
    ON DELETE CASCADE
);