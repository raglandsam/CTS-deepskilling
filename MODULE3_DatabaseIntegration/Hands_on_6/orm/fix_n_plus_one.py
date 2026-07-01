"""
TASK 3 : 87 - 90
    N+1 PROBLEM FIXING AND query analysis
================================================================================
1. IDENTIFIED PROBLEM :
   - A naive loop across Enrollment records triggers independent, sequential 
     SELECT queries for '.student' and '.course' relations on every loop pass.
   - Computational Complexity: O(1 + 2N) database network socket round-trips.

2. SYSTEM ARCHITECTURE RESOLUTION (Eager Loading Strategy):
   - Appended '.options(joinedload(Enrollment.student), joinedload(Enrollment.course))'
     to force SQLAlchemy to intercept the relationship parameters upfront.
   - Generates an explicit 'LEFT OUTER JOIN' matrix targeting 'students' and 'courses'.
   - Computational Complexity: O(1) single database packet transmission pass.

3. LOG VERIFICATION ANALYSIS:
   - Verification logs confirm one master unified SELECT query executes.
   - Zero internal side-effect lookups hit the thread pool during iteration loops.
"""
from db_init import SessionLocal, engine
from models import Base, Enrollment
from sqlalchemy.orm import joinedload

def fix_n_plus_one_88():
    session= SessionLocal()
    try:
        print("\nFixing N+! using joinedload")
        enrollments = session.query(Enrollment).options(joinedload(Enrollment.Student), joinedload(Enrollment.Course)).all()
        for enrollment in enrollments:
            print(f"Enrollment Details: {enrollment.Student.first_name} {enrollment.Student.last_name} enrolled in {enrollment.Course.course_name}")
    except Exception as e:
        print(f"\n[ERROR] Fix N+1 operation failed. Reason: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    fix_n_plus_one_88()