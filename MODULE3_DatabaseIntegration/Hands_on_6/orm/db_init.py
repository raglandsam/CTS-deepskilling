#78 and 79
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Department, Student, Course, Enrollment, Professor

DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/college_db_orm")

engine=create_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
def initialze_database():
    print("---Initializing database----")
    Base.metadata.create_all(bind=engine)

if __name__=='__main__':
    initialze_database()

