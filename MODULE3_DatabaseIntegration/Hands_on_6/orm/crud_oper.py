import datetime
from db_init import SessionLocal
from models import Department, Student, Course, Enrollment

def mass_seed_database():
    session = SessionLocal()
    try:
        print("\n1: Instantiating Departments ---")
        cs_dept = Department(dept_name="Computer Science", hod_name="Dr. Arul Raj")
        ee_dept = Department(dept_name="Electrical Engineering", hod_name="Dr. Meera Nair")
        
        session.add_all([cs_dept, ee_dept])
        session.flush()  

        print("\n2: Instantiating Courses ---")
        ds_course = Course(course_code="CS101", course_name="Data Structures", credits=4, department_id=cs_dept.department_id)
        db_course = Course(course_code="CS102", course_name="Database Systems", credits=4, department_id=cs_dept.department_id)
        ee_course = Course(course_code="EE101", course_name="Circuits & Systems", credits=3, department_id=ee_dept.department_id)
        
        session.add_all([ds_course, db_course, ee_course])
        session.flush()

        print("\n3: Instantiating Students ---")
        students_list = [
            Student(first_name="Samuel", last_name="Ragland", email="sam.r@college.edu", date_of_birth=datetime.date(2004, 6, 16), department_id=cs_dept.department_id, enrollment_year=2022),
            Student(first_name="John", last_name="Cena", email="john.cena@college.edu", date_of_birth=datetime.date(2003, 4, 12), department_id=cs_dept.department_id, enrollment_year=2022),
            Student(first_name="Steve", last_name="Smith", email="steve.s@college.edu", date_of_birth=datetime.date(2005, 11, 23), department_id=ee_dept.department_id, enrollment_year=2023),
        ]
        session.add_all(students_list)
        session.flush()

        print("\n4: Instantiating Cross-Enrollments ---")
        enrollments_list = [
            Enrollment(student_id=students_list[0].student_id, course_id=ds_course.course_id, enrollment_date=datetime.date(2022, 9, 1), grade="A"),
            Enrollment(student_id=students_list[0].student_id, course_id=db_course.course_id, enrollment_date=datetime.date(2022, 9, 1), grade="O"),
            Enrollment(student_id=students_list[1].student_id, course_id=ds_course.course_id, enrollment_date=datetime.date(2022, 9, 1), grade="B"),
            Enrollment(student_id=students_list[2].student_id, course_id=ee_course.course_id, enrollment_date=datetime.date(2023, 9, 1), grade="A"),
        ]
        session.add_all(enrollments_list)

        session.commit()
        print("\n[SUCCESS] Mass seed complete. check postgres")

    except Exception as e:
        session.rollback()
        print(f"\n[ERROR] Seed aborted, rolled back cleanly. Reason: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    mass_seed_database()