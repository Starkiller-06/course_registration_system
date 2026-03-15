from datetime import datetime
from domain.models import Student, Section, Course, CourseCode, DateRange

class StudentRepository:
    def __init__(self, db) -> None:
        self.collection = db.get_collection()
    
    def get(self, student_id: int) -> Student | None:
        data = self.collection.findOne({"_id": student_id})
        
        if not data:
            return None
        
        student = Student(id=data["_id"], name=data["name"])

        # Keep value objects updated with DB
        student.passed_courses = [CourseCode(code) for code in data.get("passed_courses", [])]
        student.enrolled_sections = data.get("enrolled_sections", [])

        return student

    def save(self, student: Student):
        student_dict = {
            "_id": student.id,
            "name": student.name,
            "passed_courses": student.passed_courses,
            "enrolled_sections": student.enrolled_sections
        }
        self.collection.update_one({"_id": student.id}, {"$set": student_dict}, upsert=True)

class SectionRepository:
    def __init__(self, db):
        self.collection = db.get_collection("sections")

    def get(self, section_id: str) -> Section | None:
        data = self.collection.find_one({"_id": section_id})
        if not data:
            return None

        # Rehydrate Value Objects
        course_code = CourseCode(data["course_code"])
        
        # MongoDB stores datetime, we need pure date for our DateRange
        start = data["term_start"].date() if isinstance(data["term_start"], datetime) else data["term_start"]
        end = data["term_end"].date() if isinstance(data["term_end"], datetime) else data["term_end"]
        term_dates = DateRange(start_date=start, end_date=end)

        section = Section(
            id=data["_id"],
            delivery_method=data["delivery_method"],
            course_code=course_code,
            capacity=data["capacity"],
            term_dates=term_dates,
            professor_id=data["professor_id"]
        )
        section.roster = data.get("roster", [])
        return section

    def save(self, section: Section):
        # Convert date to datetime for MongoDB compatibility
        start_dt = datetime.combine(section.term_dates.start_date, datetime.min.time())
        end_dt = datetime.combine(section.term_dates.end_date, datetime.min.time())

        section_dict = {
            "_id": section.id,
            "course_code": section.course_code.value,
            "capacity": section.capacity,
            "term_start": start_dt,
            "term_end": end_dt,
            "professor_id": section.professor_id,
            "roster": section.roster
        }
        self.collection.update_one({"_id": section.id}, {"$set": section_dict}, upsert=True)


class CourseRepository:
    def __init__(self, db):
        self.collection = db.get_collection("courses")

    def get(self, course_code_str: str) -> Course | None:
        data = self.collection.find_one({"_id": course_code_str})
        if not data:
            return None

        code = CourseCode(data["_id"])
        prereqs = [CourseCode(req) for req in data.get("prerequisites", [])]

        return Course(course_code=code, name=data["name"], description=data["description"], credits=data["credits"], prerequisites=prereqs)
        course_dict = {
            "_id": course.code.value,
            "name": course.name,
            "credits": course.credits,
            "prerequisites": [req.value for req in course.prerequisites]
        }
        self.collection.update_one({"_id": course.code.value}, {"$set": course_dict}, upsert=True)