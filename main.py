from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

students = []

class Student(BaseModel):
    name: str
    age: int
    score: float

@app.get("/students")
def get_students():
    return students

@app.post("/students")
def add_student(student: Student):
    students.append(student)
    return {"message": f"{student.name}님이 추가됐습니다!"}