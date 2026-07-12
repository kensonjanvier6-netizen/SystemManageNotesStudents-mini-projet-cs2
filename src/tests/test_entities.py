# Tests: Entities
#
# Tests all business rules defined in Student, Course, and Note
# domain entities. Each test class focuses on one entity only.


import unittest

from entities.student import Student, InvalidStudentError
from entities.course import Course, InvalidCourseError
from entities.note import Note, InvalidNoteError


# ================================================================
# STUDENT TESTS
# ================================================================

class TestStudent(unittest.TestCase):

    # --- valid creation ---

    def test_create_valid_student(self):
        student = Student(id="S1", matricule="MAT001", name="Kenson Janvier")
        self.assertEqual(student.id, "S1")
        self.assertEqual(student.matricule, "MAT001")
        self.assertEqual(student.name, "Kenson Janvier")

    # --- full_name ---

    def test_full_name_returns_name(self):
        student = Student(id="S1", matricule="MAT001", name="Kenson Janvier")
        self.assertEqual(student.full_name(), "Kenson Janvier")

    # --- has_matricule ---

    def test_has_matricule_returns_true_when_match(self):
        student = Student(id="S1", matricule="MAT001", name="Kenson Janvier")
        self.assertTrue(student.has_matricule("MAT001"))

    def test_has_matricule_returns_false_when_no_match(self):
        student = Student(id="S1", matricule="MAT001", name="Kenson Janvier")
        self.assertFalse(student.has_matricule("XXX"))

    # --- validation rules ---

    def test_empty_id_raises_error(self):
        with self.assertRaises(InvalidStudentError):
            Student(id="", matricule="MAT001", name="Kenson Janvier")

    def test_empty_matricule_raises_error(self):
        with self.assertRaises(InvalidStudentError):
            Student(id="S1", matricule="", name="Kenson Janvier")

    def test_empty_name_raises_error(self):
        with self.assertRaises(InvalidStudentError):
            Student(id="S1", matricule="MAT001", name="")

    # --- immutability ---

    def test_student_is_immutable(self):
        student = Student(id="S1", matricule="MAT001", name="Kenson Janvier")
        with self.assertRaises(Exception):
            student.name = "Autre Nom"


# ================================================================
# COURSE TESTS
# ================================================================

class TestCourse(unittest.TestCase):

    # --- valid creation ---

    def test_create_valid_course(self):
        course = Course(id="C1", name="Mathematiques", credits=7)
        self.assertEqual(course.id, "C1")
        self.assertEqual(course.name, "Mathematiques")
        self.assertEqual(course.credits, 7)

    # --- has_id ---

    def test_has_id_returns_true_when_match(self):
        course = Course(id="C1", name="Mathematiques", credits=7)
        self.assertTrue(course.has_id("C1"))

    def test_has_id_returns_false_when_no_match(self):
        course = Course(id="C1", name="Mathematiques", credits=7)
        self.assertFalse(course.has_id("C2"))

    # --- validation rules ---

    def test_empty_id_raises_error(self):
        with self.assertRaises(InvalidCourseError):
            Course(id="", name="Mathematiques", credits=7)

    def test_empty_name_raises_error(self):
        with self.assertRaises(InvalidCourseError):
            Course(id="C1", name="", credits=7)

    def test_zero_credits_raises_error(self):
        with self.assertRaises(InvalidCourseError):
            Course(id="C1", name="Mathematiques", credits=0)

    def test_negative_credits_raises_error(self):
        with self.assertRaises(InvalidCourseError):
            Course(id="C1", name="Mathematiques", credits=-3)

    # --- immutability ---

    def test_course_is_immutable(self):
        course = Course(id="C1", name="Mathematiques", credits=7)
        with self.assertRaises(Exception):
            course.credits = 10


# ================================================================
# NOTE TESTS
# ================================================================

class TestNote(unittest.TestCase):

    # --- valid creation ---

    def test_create_valid_note(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=85)
        self.assertEqual(note.id, "N1")
        self.assertEqual(note.value, 85)

    # --- mention ---

    def test_mention_perfect(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=80)
        self.assertEqual(note.mention(), "Perfect")

    def test_mention_perfect_max(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=100)
        self.assertEqual(note.mention(), "Perfect")

    def test_mention_good(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=72)
        self.assertEqual(note.mention(), "Good")

    def test_mention_good_min(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=60)
        self.assertEqual(note.mention(), "Good")

    def test_mention_failure(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=45)
        self.assertEqual(note.mention(), "Failure")

    def test_mention_failure_min(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=0)
        self.assertEqual(note.mention(), "Failure")

    # --- is_passing ---

    def test_is_passing_returns_true(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=60)
        self.assertTrue(note.is_passing())

    def test_is_passing_returns_false(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=59)
        self.assertFalse(note.is_passing())

    # --- belongs_to_student ---

    def test_belongs_to_student_true(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=85)
        self.assertTrue(note.belongs_to_student("S1"))

    def test_belongs_to_student_false(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=85)
        self.assertFalse(note.belongs_to_student("S2"))

    # --- belongs_to_course ---

    def test_belongs_to_course_true(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=85)
        self.assertTrue(note.belongs_to_course("C1"))

    def test_belongs_to_course_false(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=85)
        self.assertFalse(note.belongs_to_course("C2"))

    # --- validation rules ---

    def test_empty_id_raises_error(self):
        with self.assertRaises(InvalidNoteError):
            Note(id="", student_id="S1", course_id="C1", value=85)

    def test_empty_student_id_raises_error(self):
        with self.assertRaises(InvalidNoteError):
            Note(id="N1", student_id="", course_id="C1", value=85)

    def test_empty_course_id_raises_error(self):
        with self.assertRaises(InvalidNoteError):
            Note(id="N1", student_id="S1", course_id="", value=85)

    def test_value_above_100_raises_error(self):
        with self.assertRaises(InvalidNoteError):
            Note(id="N1", student_id="S1", course_id="C1", value=101)

    def test_value_below_0_raises_error(self):
        with self.assertRaises(InvalidNoteError):
            Note(id="N1", student_id="S1", course_id="C1", value=-1)

    # --- immutability ---

    def test_note_is_immutable(self):
        note = Note(id="N1", student_id="S1", course_id="C1", value=85)
        with self.assertRaises(Exception):
            note.value = 100


if __name__ == "__main__":
    unittest.main()