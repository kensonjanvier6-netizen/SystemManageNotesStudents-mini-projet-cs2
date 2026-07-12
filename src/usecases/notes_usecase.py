# Application Layer: Note Use Cases
#
# This module defines all use cases related to the Note entity.
# It imports all repositories from the repositories layer —
# it does NOT define them here.


from entities.notes import Note
from repository.notes_repository import NoteRepository
from repository.students_repository import StudentRepository
from repository.courses_repository import CourseRepository


# ================================================================
# USE CASE 1: AssignNote
# ================================================================

class AssignNote:
    """
    Use case: assign a grade to a student for a specific course.

    Business rules enforced here:
    - The student must exist in the system.
    - The course must exist in the system.
    - A note with the same id must not already exist.
    - All value validations are delegated to the Note entity.
    """

    def __init__(
        self,
        note_repository: NoteRepository,
        student_repository: StudentRepository,
        course_repository: CourseRepository,
    ):
        self._notes    = note_repository
        self._students = student_repository
        self._courses  = course_repository

    def execute(
        self,
        note_id: str,
        student_id: str,
        course_id: str,
        value: float,
    ) -> Note:
        """
        Creates and persists a new Note.

        Args:
            note_id:    unique identifier for the note.
            student_id: id of the student receiving the grade.
            course_id:  id of the course the grade is for.
            value:      numeric grade between 0 and 100.

        Returns:
            The newly created Note instance.

        Raises:
            ValueError: if student or course does not exist,
                        or if a note with the same id already exists.
            InvalidNoteError: if the value is outside 0-100.
        """

        # Rule 1: the student must exist
        if not self._students.exists(student_id):
            raise ValueError(f"No student found with id '{student_id}'.")

        # Rule 2: the course must exist
        if not self._courses.exists(course_id):
            raise ValueError(f"No course found with id '{course_id}'.")

        # Rule 3: no duplicate note id
        if self._notes.exists(note_id):
            raise ValueError(f"A note with id '{note_id}' already exists.")

        # Delegate value validation to the domain entity
        note = Note(
            id=note_id,
            student_id=student_id,
            course_id=course_id,
            value=value,
        )

        self._notes.save(note)
        return note


# ================================================================
# USE CASE 2: GetStudentNotes
# ================================================================

class GetStudentNotes:
    """
    Use case: retrieve all notes for a given student.

    Business rules enforced here:
    - The student must exist in the system.
    """

    def __init__(
        self,
        note_repository: NoteRepository,
        student_repository: StudentRepository,
    ):
        self._notes    = note_repository
        self._students = student_repository

    def execute(self, student_id: str) -> list[Note]:
        """
        Returns all notes belonging to the given student.

        Args:
            student_id: the unique identifier of the student.

        Returns:
            A list of Note instances (may be empty).

        Raises:
            ValueError: if no student with that id is found.
        """

        if not self._students.exists(student_id):
            raise ValueError(f"No student found with id '{student_id}'.")

        return self._notes.find_by_student(student_id)


# ================================================================
# USE CASE 3: ComputeGPA
# ================================================================

class ComputeGPA:
    """
    Use case: compute the simple average (GPA) of a student.

    Business rules enforced here:
    - The student must exist in the system.
    - If the student has no notes, GPA is 0.0 by convention.
    - GPA is computed as a simple arithmetic mean (no weighting).
    """

    def __init__(
        self,
        note_repository: NoteRepository,
        student_repository: StudentRepository,
    ):
        self._notes    = note_repository
        self._students = student_repository

    def execute(self, student_id: str) -> float:
        """
        Computes and returns the GPA of the given student.

        Args:
            student_id: the unique identifier of the student.

        Returns:
            A float representing the simple average of all grades.
            Returns 0.0 if the student has no notes yet.

        Raises:
            ValueError: if no student with that id is found.
        """

        if not self._students.exists(student_id):
            raise ValueError(f"No student found with id '{student_id}'.")

        notes = self._notes.find_by_student(student_id)

        if not notes:
            return 0.0

        total = sum(note.value for note in notes)
        return round(total / len(notes), 2)