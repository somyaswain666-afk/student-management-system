from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models

import schemas

import crud

import chat_service

from database import engine, Base, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management System",
    description="Student Management System with FastAPI and Gemini AI",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Student Management System API is running"}


@app.post("/students", response_model=schemas.StudentResponse)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_student(db, student)


@app.get("/students", response_model=list[schemas.StudentResponse])
def read_students(
    db: Session = Depends(get_db)
):
    return crud.get_students(db)


@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db)
):
    updated_student = crud.update_student(
        db,
        student_id,
        student
    )

    if updated_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return updated_student


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    deleted_student = crud.delete_student(
        db,
        student_id
    )

    if deleted_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }


@app.post("/chat")
def chat(
    request: schemas.ChatRequest,
    db: Session = Depends(get_db)
):
    answer = chat_service.process_chat(
        request.question,
        db
    )

    return {
        "question": request.question,
        "answer": answer
    }