from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name = Column(String(50), nullable=False)
    hod_name = Column(String(50), nullable=False)
    budget = Column(Numeric(12, 2))  # Fixed: Added valid datatype

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
