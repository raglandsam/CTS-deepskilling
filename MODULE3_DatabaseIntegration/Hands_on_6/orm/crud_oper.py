import datetime
from db_init import SessionLocal
from models import Department, Student, Course, Enrollment, CourseSchedule

#81 and 82 Seeding the database with initial data
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


#83 function to read students in Computer Science department
def read_83():
    session=SessionLocal()
    try:
        print("\nReading students in Computer Science")
        cs_students=session.query(Student).join(Department).filter(Department.dept_name=='Computer Science').all()
        for student in cs_students:
            print(f"Student : {student.first_name}\t{student.last_name}\t{student.email}\t{student.date_of_birth}\t{student.enrollment_year}")
    except Exception as e:
        print(f"\n[ERROR] Read operation failed. Reason: {e}")
    finally:   
        session.close()
#84 function to read ALL ENROLLMENTS and print students name and course name
def read_84():
    session= SessionLocal()
    try :
         print("\nReading all enrollments with student names and course names")
         read_result=session.query(Enrollment).join(Student).join(Course).all()
         for enrollment in read_result:
             print(f"Enrollment Details {enrollment.Student.first_name} {enrollment.Student.last_name} enrolled in {enrollment.Course.course_name}")
    except Exception as e:
        print(f"\n[ERROR] Read operation failed. Reason: {e}")
    finally:
        session.close()

def update_85():
    session=SessionLocal()
    try :
        res= session.query(Student).filter(Student.email == "steve.s@college.edu").first()
        if res:
            print(f"before updation {res.email}")
            res.email="steve.smith@college.edu"
            session.commit()
            print(f"after updation {res.email}")
        else:
            return "No student found with the specified email."
    except Exception as e:
        session.rollback()
        print(f"\n[ERROR] Update operation failed. Reason: {e}")
    finally:
        session.close()

def delete_86():
    session=SessionLocal()
    try:
        res= session.query(Enrollment).filter(Enrollment.enrollment_id==1).first()
        if res:
            print(f"to be deleted from enrollments {res.enrollment_id}")
            session.delete(res)
            session.commit()
        else:
            return "No enrollment found with the specified ID."
    except Exception as e:  
        session.rollback()
        print(f"\n[ERROR] Delete operation failed. Reason: {e}")
    finally:
        session.close()



if __name__ == "__main__":
    #mass_seed_database()
    #read_83()
    #read_84()
    #update_85()
    delete_86()