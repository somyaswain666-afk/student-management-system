from sqlalchemy import Column, Integer, String, Float, Date

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    department = Column(String, nullable=False)
    gpa = Column(Float, nullable=False)
    enrollment_date = Column(Date, nullable=False)