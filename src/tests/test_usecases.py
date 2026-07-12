import sys
sys.path.insert(0, r"C:\Users\kenso\kenson-janvier-mini-projet-cs2\SRC")
import os
import unittest


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
# STUDENT USE CASE TESTS
# ================================================================

class TestCreateStudent(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryStudentRepository()
        self.use_case = CreateStudent(self.repo)

    def test_create_student_success(self):
        student = self.use_case.execute("S1", "MAT001", "Kenson Janvier")
        self.assertEqual(student.id, "S1")
        self.assertEqual(student.matricule, "MAT001")

    def test_create_student_persisted_in_repo(self):
        self.use_case.execute("S1", "MAT001", "Kenson Janvier")
        self.assertTrue(self.repo.exists("S1"))

    def test_create_student_duplicate_id_raises_error(self):
        self.use_case.execute("S1", "MAT001", "Kenson Janvier")
        with self.assertRaises(ValueError):
            self.use_case.execute("S1", "MAT002", "Autre Nom")

    def test_create_student_duplicate_matricule_raises_error(self):
        self.use_case.execute("S1", "MAT001", "Kenson Janvier")
        with self.assertRaises(ValueError):
            self.use_case.execute("S2", "MAT001", "Autre Nom")


class TestGetStudent(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryStudentRepository()
        CreateStudent(self.repo).execute("S1", "MAT001", "Kenson Janvier")
        self.use_case = GetStudent(self.repo)

    def test_get_existing_student(self):
        student = self.use_case.execute("S1")
        self.assertEqual(student.id, "S1")

    def test_get_nonexistent_student_raises_error(self):
        with self.assertRaises(ValueError):
            self.use_case.execute("UNKNOWN")


# ================================================================
# COURSE USE CASE TESTS
# ================================================================

class TestCreateCourse(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryCourseRepository()
        self.use_case = CreateCourse(self.repo)

    def test_create_course_success(self):
        course = self.use_case.execute("C1", "Mathematiques", 7)
        self.assertEqual(course.id, "C1")
        self.assertEqual(course.credits, 7)

    def test_create_course_persisted_in_repo(self):
        self.use_case.execute("C1", "Mathematiques", 7)
        self.assertTrue(self.repo.exists("C1"))

    def test_create_course_duplicate_id_raises_error(self):
        self.use_case.execute("C1", "Mathematiques", 7)
        with self.assertRaises(ValueError):
            self.use_case.execute("C1", "Algorithmique", 5)


class TestGetCourse(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryCourseRepository()
        CreateCourse(self.repo).execute("C1", "Mathematiques", 7)
        self.use_case = GetCourse(self.repo)
class TestGetCourse(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryCourseRepository()
        CreateCourse(self.repo).execute("C1", "Mathematiques", 7)
        self.use_case = GetCourse(self.repo)

    def test_get_existing_course(self):
        course = self.use_case.execute("C1")
        self.assertEqual(course.id, "C1")

    def test_get_nonexistent_course_raises_error(self):
        with self.assertRaises(ValueError):
            self.use_case.execute("UNKNOWN")


class TestAssignNote(unittest.TestCase):

    def setUp(self):
        self.student_repo = InMemoryStudentRepository()
        self.course_repo  = InMemoryCourseRepository()
        self.note_repo    = InMemoryNoteRepository()
        CreateStudent(self.student_repo).execute("S1", "MAT001", "Kenson Janvier")
        CreateCourse(self.course_repo).execute("C1", "Mathematiques", 7)
        self.use_case = AssignNote(self.note_repo, self.student_repo, self.course_repo)

    def test_assign_note_success(self):
        note = self.use_case.execute("N1", "S1", "C1", 85)
        self.assertEqual(note.id, "N1")
        self.assertEqual(note.value, 85)

    def test_assign_note_persisted_in_repo(self):
        self.use_case.execute("N1", "S1", "C1", 85)
        self.assertTrue(self.note_repo.exists("N1"))

    def test_assign_note_student_not_found_raises_error(self):
        with self.assertRaises(ValueError):
            self.use_case.execute("N1", "UNKNOWN", "C1", 85)

    def test_assign_note_course_not_found_raises_error(self):
        with self.assertRaises(ValueError):
            self.use_case.execute("N1", "S1", "UNKNOWN", 85)

    def test_assign_note_duplicate_id_raises_error(self):
        self.use_case.execute("N1", "S1", "C1", 85)
        with self.assertRaises(ValueError):
            self.use_case.execute("N1", "S1", "C1", 72)


class TestGetStudentNotes(unittest.TestCase):

    def setUp(self):
        self.student_repo = InMemoryStudentRepository()
        self.course_repo  = InMemoryCourseRepository()
        self.note_repo    = InMemoryNoteRepository()
        CreateStudent(self.student_repo).execute("S1", "MAT001", "Kenson Janvier")
        CreateCourse(self.course_repo).execute("C1", "Mathematiques", 7)
        assign = AssignNote(self.note_repo, self.student_repo, self.course_repo)
        assign.execute("N1", "S1", "C1", 85)
        assign.execute("N2", "S1", "C1", 72)
        self.use_case = GetStudentNotes(self.note_repo, self.student_repo)

    def test_get_notes_returns_all_notes(self):
        notes = self.use_case.execute("S1")
        self.assertEqual(len(notes), 2)

    def test_get_notes_student_not_found_raises_error(self):
        with self.assertRaises(ValueError):
            self.use_case.execute("UNKNOWN")

    def test_get_notes_empty_when_no_notes(self):
        CreateStudent(self.student_repo).execute("S2", "MAT002", "Autre Nom")
        notes = self.use_case.execute("S2")
        self.assertEqual(notes, [])


class TestComputeGPA(unittest.TestCase):

    def setUp(self):
        self.student_repo = InMemoryStudentRepository()
        self.course_repo  = InMemoryCourseRepository()
        self.note_repo    = InMemoryNoteRepository()
        CreateStudent(self.student_repo).execute("S1", "MAT001", "Kenson Janvier")
        CreateCourse(self.course_repo).execute("C1", "Mathematiques", 7)
        CreateCourse(self.course_repo).execute("C2", "Algorithmique", 5)
        assign = AssignNote(self.note_repo, self.student_repo, self.course_repo)
        assign.execute("N1", "S1", "C1", 85)
        assign.execute("N2", "S1", "C2", 72)
        assign.execute("N3", "S1", "C1", 45)
        self.use_case = ComputeGPA(self.note_repo, self.student_repo)

    def test_compute_gpa_correct_average(self):
        gpa = self.use_case.execute("S1")
        self.assertEqual(gpa, 67.33)

    def test_compute_gpa_returns_zero_when_no_notes(self):
        CreateStudent(self.student_repo).execute("S2", "MAT002", "Autre Nom")
        gpa = self.use_case.execute("S2")
        self.assertEqual(gpa, 0.0)

    def test_compute_gpa_student_not_found_raises_error(self):
        with self.assertRaises(ValueError):
            self.use_case.execute("UNKNOWN")


if __name__ == "__main__":
    unittest.main()