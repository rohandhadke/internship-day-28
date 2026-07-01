from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student CRUD API")


# -----------------------------
# Create Student
# -----------------------------
@app.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate,
                   db: Session = Depends(get_db)):

    new_student = models.Student(
        name=student.name,
        email=student.email,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# -----------------------------
# Get All Students
# -----------------------------
@app.get("/students", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


# -----------------------------
# Get Student By ID
# -----------------------------
@app.get("/students/{student_id}",
         response_model=schemas.StudentResponse)
def get_student(student_id: int,
                db: Session = Depends(get_db)):

    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# -----------------------------
# Update Student
# -----------------------------
@app.put("/students/{student_id}",
         response_model=schemas.StudentResponse)
def update_student(student_id: int,
                   updated_data: schemas.StudentCreate,
                   db: Session = Depends(get_db)):

    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = updated_data.name
    student.email = updated_data.email
    student.course = updated_data.course

    db.commit()
    db.refresh(student)

    return student


# -----------------------------
# Delete Student
# -----------------------------
@app.delete("/students/{student_id}")
def delete_student(student_id: int,
                   db: Session = Depends(get_db)):

    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }