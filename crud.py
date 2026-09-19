from sqlalchemy import or_,desc

from sqlalchemy.orm import Session

import models
import schemas


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(db: Session):
    return db.query(models.Student).all()


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()


def update_student(
    db: Session,
    student_id: int,
    student: schemas.StudentUpdate
):
    db_student = get_student(db, student_id)

    if db_student is None:
        return None

    update_data = student.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_student, field, value)

    db.commit()
    db.refresh(db_student)

    return db_student


def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)

    if db_student is None:
        return None

    db.delete(db_student)
    db.commit()

    return db_student
def search_students(db: Session, search_term: str):
    words = search_term.lower().split()

    stop_words = {
        "what", "is", "the", "a", "an", "of",
        "for", "student", "students", "tell", "me",
        "about", "please", "give", "show", "has",
        "who", "with", "their", "his", "her"
    }

    useful_words = []

    for word in words:

        word = word.strip("?,.\"")

        # Rahul's → Rahul
        if word.endswith("'s"):
            word = word[:-2]

        word = word.strip("'")

        if word and word not in stop_words:
            useful_words.append(word)

    if not useful_words:
        return []

    filters = []

    for word in useful_words:

        filters.append(
            models.Student.name.ilike(f"%{word}%")
        )

        filters.append(
            models.Student.student_id.ilike(f"%{word}%")
        )

        filters.append(
            models.Student.department.ilike(f"%{word}%")
        )

    return db.query(models.Student).filter(
        or_(*filters)
    ).all()

    stop_words = {
        "what", "is", "the", "a", "an", "of",
        "for", "student", "students", "tell", "me",
        "about", "please", "give", "show", "has",
        "who", "with", "their", "his", "her"
    }

    useful_words = [
        word.strip("?,.'\"")
        for word in words
        if word.strip("?,.'\"") not in stop_words
    ]

    if not useful_words:
        return []

    filters = []

    for word in useful_words:
        filters.append(models.Student.name.ilike(f"%{word}%"))
        filters.append(models.Student.student_id.ilike(f"%{word}%"))
        filters.append(models.Student.department.ilike(f"%{word}%"))

    return db.query(models.Student).filter(
        or_(*filters)
    ).all()
def get_top_gpa_student(db: Session):

    return db.query(models.Student).order_by(

        desc(models.Student.gpa)

    ).first()

def count_students_by_department(db: Session, department: str):
    return db.query(models.Student).filter(
        models.Student.department.ilike(department)
    ).count()
def get_average_gpa(db: Session):

    students = db.query(models.Student).all()

    if not students:

        return None

    total_gpa = sum(student.gpa for student in students)

    return total_gpa / len(students)
def get_students_by_department(db: Session, department: str):

    return db.query(models.Student).filter(

        models.Student.department.ilike(department)

    ).all()
def get_departments(db: Session):

    return db.query(models.Student.department).distinct().all()