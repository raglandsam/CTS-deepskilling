#TASK 3 IDENTIFYING AND FIXING THE N+1 PROPBLEM 

#imports
from tokenize import Number

import psycopg2
import time

DB_PARAMS= {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'sampostgres',
    'dbname': 'college_db',
    'port': '5432'
}
#56 USING THE N+1 SIMULATION
def run_n1_simulation():
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # Start timing
        start_time = time.perf_counter()
        query_counter=0
        # Execute the query that simulates the N+1 problem
        cursor.execute("SELECT student_id, course_id from enrollments;")
        # Fetch all results
        enrollments = cursor.fetchall()
        query_counter+=1
        for row in enrollments:
            student_id=row[0]
            cursor.execute(f"SELECT first_name, last_name FROM students WHERE student_id = {student_id}") 
            student_info=cursor.fetchone()
            query_counter+=1


        # End timing
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print("N+1 QUERY STATS")

        print(f"Query executed in {execution_time:.4f} seconds.")
        print(f"Number of records fetched: {len(enrollments)}")
        print(f"Number of queries executed: {query_counter}")
    except Exception as e:
        print(f"An error occurred: {e.message}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
#57 USING JOIN TO FIX THE N+1 PROBLEM
def using_join() :
    try :
        conn=psycopg2.connect(**DB_PARAMS)
        cursor=conn.cursor()
        start_time=time.perf_counter()
        query_counter=0
        cursor.execute("SELECT s.first_name, s.last_name, c.course_name FROM enrollments e join students s on e.student_id=s.student_id join courses c on e.course_id=c.course_id;")
        results = cursor.fetchall()
        query_counter+=1
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print("JOIN QUERY STATS")
        print(f"Join query executed in {execution_time:.4f} seconds.")
        print(f"Number of records fetched: {len(results)}")
        print(f"Number of queries executed: {query_counter}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    run_n1_simulation()
    using_join()
#58 stats 
#N+1 QUERY STATS
#Query executed in 0.0168 seconds.
#Number of records fetched: 13
#Number of queries executed: 14

#JOIN QUERY STATS
#Join query executed in 0.0237 seconds.
#Number of records fetched: 13
#Number of queries executed: 1

#59
#in a real application with 10,000 enrollments, there would be 1 query first to fetch all the 10,000 enrollments,
#then, 10,000 enrollments are looped through which would be a total of 1+10,000 queries (10,001) executed, lagging performance by a large margin.
