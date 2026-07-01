#75 76 77
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Boolean, Time
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name = Column(String(50), nullable=False)
    hod_name = Column(String(50), nullable=False)
    budget = Column(Numeric(12, 2)) 

    Students = relationship('Student', back_populates='Department')
    Courses = relationship('Course', back_populates='Department')
    Professors = relationship('Professor', back_populates='Department')



class Student(Base):
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(60), unique=True)
    date_of_birth = Column(Date, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.department_id'), nullable=False)
    enrollment_year = Column(Integer, nullable=False)

    #Hands on 7 : task 2: 98
    is_Active = Column(Boolean, nullable=False , server_default='true')
    Department = relationship('Department', back_populates='Students')
    Enrollments = relationship('Enrollment', back_populates='Student')


class Course(Base):
    __tablename__ = 'courses'
    
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(10), unique=True, nullable=False)
    course_name = Column(String(100), nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.department_id', ondelete='CASCADE'), nullable=False)

    Department = relationship('Department', back_populates='Courses')
    Enrollments = relationship("Enrollment", back_populates="Course")
    CourseSchedule = relationship("CourseSchedule", back_populates="Course")

#Hands on 7 : task 2: 102 : Cretaed a new table for course schedule to store the schedule of each course
class CourseSchedule(Base):
    __tablename__ = 'course_schedules'
    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    day_of_week = Column(String(15), nullable=False)     #monday tuesday or sm like dat
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room_number = Column(String(20), nullable=False)

    Course=relationship("Course",back_populates="CourseSchedule")

class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    grade = Column(String(2), nullable=True) 
    
    Student = relationship("Student", back_populates="Enrollments")
    Course = relationship("Course", back_populates="Enrollments")


class Professor(Base):
    __tablename__ = 'professors'
    
    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    prof_name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)
    department_id = Column(Integer, ForeignKey('departments.department_id'), nullable=False)

    Department = relationship("Department", back_populates='Professors')
