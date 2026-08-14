import sys
sys.path.insert(0, r"C:\Users\kenso\kenson-janvier-mini-projet-cs2\SRC")

from entities.students import Student
from entities.courses import Course
from entities.notes import Note

from repository.students_repository import StudentRepository
from repository.courses_repository import CourseRepository
from repository.notes_repository import NoteRepository

from usecases.students_usecase import CreateStudent, GetStudent
from usecases.courses_usecase import CreateCourse, GetCourse
from usecases.notes_usecase import AssignNote, GetStudentNotes, ComputeGPA

from typing import Optional


# ================================================================
# IN-MEMORY IMPLEMENTATIONS
# ================================================================

class InMemoryStudentRepository(StudentRepository):
    def __init__(self):
        self._store: dict[str, Student] = {}

    def save(self, student: Student) -> None:
        self._store[student.id] = student

    def find_by_id(self, student_id: str) -> Optional[Student]:
        return self._store.get(student_id)

    def find_by_matricule(self, matricule: str) -> Optional[Student]:
        for student in self._store.values():
            if student.has_matricule(matricule):
                return student
        return None

    def exists(self, student_id: str) -> bool:
        return student_id in self._store


class InMemoryCourseRepository(CourseRepository):
    def __init__(self):
        self._store: dict[str, Course] = {}

    def save(self, course: Course) -> None:
        self._store[course.id] = course

    def find_by_id(self, course_id: str) -> Optional[Course]:
        return self._store.get(course_id)

    def exists(self, course_id: str) -> bool:
        return course_id in self._store


class InMemoryNoteRepository(NoteRepository):
    def __init__(self):
        self._store: dict[str, Note] = {}

    def save(self, note: Note) -> None:
        self._store[note.id] = note

    def find_by_id(self, note_id: str) -> Optional[Note]:
        return self._store.get(note_id)

    def find_by_student(self, student_id: str) -> list[Note]:
        return [n for n in self._store.values() if n.belongs_to_student(student_id)]

    def exists(self, note_id: str) -> bool:
        return note_id in self._store


# ================================================================
# DEMO
# ================================================================

# Setup repositories
student_repo = InMemoryStudentRepository()
course_repo  = InMemoryCourseRepository()
note_repo    = InMemoryNoteRepository()

# Setup use cases
create_student     = CreateStudent(student_repo)
create_course      = CreateCourse(course_repo)
assign_note        = AssignNote(note_repo, student_repo, course_repo)
get_student_notes  = GetStudentNotes(note_repo, student_repo)
compute_gpa        = ComputeGPA(note_repo, student_repo)

print("=" * 50)
print("   System manage note students")
print("=" * 50)

# step 1
student = create_student.execute(
    student_id="202504039",
    matricule="MAT141",
    name="Kenson Janvier"
)
print(f"\n✅ student  : {student.full_name()}")
print(f"   ID            : {student.id}")
print(f"   Matricule     : {student.matricule}")

# step 2 
course = create_course.execute(
    course_id="C1",
    name="Algorithmique",
    credits=5
)
print(f"\n✅ course      : {course.name}")
print(f"   ID            : {course.id}")
print(f"   course credits      : {course.credits}")

# step 3 
note = assign_note.execute(
    note_id="N1",
    student_id="202504039",
    course_id="C1",
    value=85
)
print(f"\n✅ Note     : {note.value} / 100")
print(f"   Mention       : {note.mention()}")
print(f"   succes          : {'passing' if note.is_passing() else 'failure'}")

# step 4 
print(f"\n📋 student Note {student.full_name()} :")
print("-" * 50)
notes = get_student_notes.execute("202504039")
for n in notes:
    print(f"   course: {n.course_id} | Note: {n.value} | Mention: {n.mention()}")

# step 5 — calculate GPA
gpa = compute_gpa.execute("202504039")
print(f"\n📊 compute (GPA)  : {gpa} / 100")
print("=" * 50)
