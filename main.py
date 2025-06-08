from fastapi import FastAPI
from pydantic import BaseModel, conint, constr
from typing import List

app = FastAPI()

# 점수 기준표
GRADE_TO_POINT = {
    "A+": 4.5, "A": 4.0,
    "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0,
    "D+": 1.5, "D": 1.0,
    "F": 0.0
}

# 한 과목 정보
class Course(BaseModel):
    course_code: str
    course_name: str
    credits: conint(gt=0)
    grade: constr(regex="^(A\\+|A|B\\+|B|C\\+|C|D\\+|D|F)$")

# 전체 학생 정보
class StudentRequest(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

@app.post("/score")
def calculate_score(data: StudentRequest):
    total_credits = sum(course.credits for course in data.courses)
    total_points = sum(course.credits * GRADE_TO_POINT[course.grade] for course in data.courses)

    gpa_raw = total_points / total_credits if total_credits > 0 else 0.0
    gpa = round(gpa_raw + 1e-8, 2)

    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": gpa,
            "total_credits": total_credits
        }
    }
