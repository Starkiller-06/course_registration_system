from dataclasses import dataclass
from typing import List
from datetime import date

# Value objects:
@dataclass(frozen=True)
class CourseCode:
    value: str

@dataclass(frozen=True)
class DateRange:
    start_date: date
    end_date: date
    
    def __post_init__(self):
        if self.start_date > self.end_date:
            raise ValueError("Start date must be strictly before the end date.")

# Entities
class Professor:
    def __init__(self, id: int, name: str, department: str):
        self.id = id
        self.name = name
        self.department = department


class Course:
    def __init__(self, course_code: CourseCode, name: str, credits: int, description: str, prerequisites: List[CourseCode]):
        self.course_code = course_code
        self.name = name
        self.credits = credits
        self.description = description
        self.prerequisites = prerequisites

class Section:
    def __init__(self, id: int, name: str, capacity: int, delivery_method: str, term_dates: DateRange, professor_id: int):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.delivery_method = delivery_method
        self.term_dates = term_dates
        self.professor_id = professor_id
        self.roster: List[int] = []
    
    def add_student(self, student_id: int):
        if len(self.roster) >= self.capacity:
            raise ValueError("Section capacity reached. Cannot enroll student :(")
        if student_id not in self.roster:
            self.roster.append(student_id)
    
    def remove_student(self, student_id):
        if student_id in self.roster:
            self.roster.remove(student_id)
        
class Student:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.enrolled_sections: List[int] = []
        self.passed_courses: List[CourseCode] = [] 

    def record_passed_course(self, course_code: CourseCode):
        if course_code not in self.passed_courses:
            self.passed_courses.append(course_code)

    def has_passed_prerequisites(self, required_courses: List[CourseCode]) -> bool:
        return all(req in self.passed_courses for req in required_courses) # IDK 
    
