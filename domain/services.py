class RegistrationService:
    def __init__(self, student_repo, section_repo, course_repo) -> None:
        self.student_repo = student_repo
        self.section_repo = section_repo
        self.course_repo = course_repo
    
    def register_student_for_section(self, student_id: int, section_id: int):
        student = self.student_repo.get(student_id)
        section = self.section_repo.get(section_id)

        if not student:
            raise ValueError(f"Student {student_id} not found")
        if not section:
            raise ValueError(f"Section {section_id} not found")
        
        course = self.course_repo.get(section.course_id)

        if not course:
            raise ValueError(f"Course {section.course_id} not found")
        
        # Ensure the student has taken the required courses
        if not student.has_passed_prerequisites():
            raise ValueError(f"Student '{student_id}' does not meet prerequisites for {course.code.value}.")
        
        section.add_student(student.id)

        if section.id not in student.enrolled_sections:
            student.enrolled_sections.append(section.id)

        self.section_repo.save()
        self.student_repo.save()

        return f"Success: {student.name} enrolled in {section_id}!"
