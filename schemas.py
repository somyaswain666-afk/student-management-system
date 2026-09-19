from datetime import date

from pydantic import BaseModel, Field


class StudentBase(BaseModel):
    student_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=16, le=100)
    gender: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    gpa: float = Field(..., ge=0, le=10)
    enrollment_date: date


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    student_id: str | None = Field(default=None, min_length=1)
    name: str | None = Field(default=None, min_length=1)
    age: int | None = Field(default=None, ge=16, le=100)
    gender: str | None = Field(default=None, min_length=1)
    department: str | None = Field(default=None, min_length=1)
    gpa: float | None = Field(default=None, ge=0, le=10)
    enrollment_date: date | None = None


class StudentResponse(StudentBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)