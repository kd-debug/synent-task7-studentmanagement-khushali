from fastapi import FastAPI, Request, Form, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
import os
import csv
import io
from typing import List, Optional
from datetime import datetime

app = FastAPI()

DATA_FILE = "students.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


def load_students():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)


def calculate_grade(cgpa: float) -> str:
    if cgpa >= 9.0: return "A+"
    elif cgpa >= 8.0: return "A"
    elif cgpa >= 7.0: return "B"
    elif cgpa >= 6.0: return "C"
    elif cgpa >= 5.0: return "D"
    else: return "F"


class Student(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    course: str
    year: int
    gpa: float
    grade: Optional[str] = None
    enrollment_date: Optional[str] = None


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    students = load_students()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"students": students}
    )


@app.get("/api/students")
async def get_students():
    return load_students()


@app.post("/api/students")
async def create_student(student: Student):
    students = load_students()
    if not students:
        student.id = 1
    else:
        student.id = max(s["id"] for s in students) + 1
    student.enrollment_date = datetime.now().isoformat()
    student.grade = calculate_grade(student.gpa)
    students.append(student.model_dump())
    save_students(students)
    return student


@app.put("/api/students/{student_id}")
async def update_student(student_id: int, updated_student: Student):
    students = load_students()
    for i, s in enumerate(students):
        if s["id"] == student_id:
            updated_data = updated_student.model_dump()
            updated_data["id"] = student_id
            updated_data["enrollment_date"] = s["enrollment_date"]
            updated_data["grade"] = calculate_grade(updated_data["gpa"])
            students[i] = updated_data
            save_students(students)
            return updated_data
    raise HTTPException(status_code=404, detail="Student not found")


@app.get("/api/export/csv")
async def export_csv(search: str = ""):
    students = load_students()
    
    # Apply search filter if query is provided
    if search:
        search_lower = search.lower()
        students = [
            s for s in students 
            if (search_lower in s["name"].lower() or 
                search_lower in s["email"].lower() or 
                search_lower in s["course"].lower())
        ]
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "name", "email", "course", "year", "gpa", "grade", "enrollment_date"])
    writer.writeheader()
    writer.writerows(students)
    
    response = StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students_records.csv"}
    )
    return response


@app.post("/api/import/csv")
async def import_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    content = await file.read()
    decoded = content.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    
    students = load_students()
    new_id = max([s["id"] for s in students], default=0) + 1
    
    imported_count = 0
    for row in reader:
        try:
            gpa = float(row["gpa"])
            new_student = {
                "id": new_id,
                "name": row["name"],
                "email": row["email"],
                "course": row["course"],
                "year": int(row["year"]),
                "gpa": gpa,
                "grade": calculate_grade(gpa),
                "enrollment_date": datetime.now().isoformat()
            }
            students.append(new_student)
            new_id += 1
            imported_count += 1
        except (KeyError, ValueError):
            continue
            
    save_students(students)
    return {"message": f"Successfully imported {imported_count} students"}


@app.delete("/api/students/{student_id}")
async def delete_student(student_id: int):
    students = load_students()
    students = [s for s in students if s["id"] != student_id]
    save_students(students)
    return {"message": "Student deleted successfully"}


@app.get("/api/statistics")
async def get_statistics():
    students = load_students()
    if not students:
        return {
            "total": 0,
            "avg_gpa": 0,
            "courses": {},
            "years": {}
        }
    total = len(students)
    avg_gpa = sum(s["gpa"] for s in students) / total
    courses = {}
    years = {}
    for s in students:
        courses[s["course"]] = courses.get(s["course"], 0) + 1
        years[s["year"]] = years.get(s["year"], 0) + 1
    
    return {
        "total": total,
        "avg_gpa": round(avg_gpa, 2),
        "courses": courses,
        "years": years
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
