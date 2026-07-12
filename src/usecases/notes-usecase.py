# Application Layer: Note Use Cases
#
# This module defines the Repository interface (port) and all
# use cases related to the Note entity, including grade assignment,
# retrieval, and GPA computation.

from abc import ABC, abstractmethod
from typing import Optional
from domain.note import Note, InvalidNoteError
from use_cases.student_use_cases import StudentRepository
from use_cases.course_use_cases import CourseRepository


# ================================================================
# REPOSITORY INTERFACE (Port)
# ================================================================

class NoteRepository(ABC):
    """
    Abstract interface for Note persistence.
    """

    @abstractmethod
    def save(self, note: Note) -> None:
        """Persist a new note or update an existing one."""
        pass

    @abstractmethod
    def find_by_id(self, note_id: str) -> Optional[Note]:
        """Return a Note by its id, or None if not found."""
        pass

    @abstractmethod
    def find_by_student(self, student_id: str) -> list[Note]:
        """Return all notes belonging to a given student."""
        pass

    @abstractmethod
    def exists(self, note_id: str) -> bool:
        """Return True if a note with the given id already exists."""
        pass


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
            InvalidNoteError: if the value is outside 0–100.
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


# ================================================================
# IN-MEMORY IMPLEMENTATION (for testing / manual verification)
# ================================================================

class InMemoryNoteRepository(NoteRepository):
    """
    Simple in-memory implementation of NoteRepository.
    """

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
# Usage example
# ================================================================
from use_cases.student_use_cases import InMemoryStudentRepository, CreateStudent
from use_cases.course_use_cases  import InMemoryCourseRepository,  CreateCourse

student_repo = InMemoryStudentRepository()
course_repo  = InMemoryCourseRepository()
note_repo    = InMemoryNoteRepository()

# Setup
CreateStudent(student_repo).execute("202504039", "MAT141", "Kenson Janvier")
CreateCourse(course_repo).execute("C1", "Mathematiques", 7)
CreateCourse(course_repo).execute("C2", "Algorithmique", 5)

# Assign notes
assign = AssignNote(note_repo, student_repo, course_repo)
assign.execute("N1", "202504039", "C1", 85)
assign.execute("N2", "202504039", "C2", 72)
assign.execute("N3", "202504039", "C1", 45)

# Get all notes
notes = GetStudentNotes(note_repo, student_repo).execute("202504039")
for note in notes:
    print(f"Course: {note.course_id} | Value: {note.value} | Mention: {note.mention()}")

# Compute GPA
gpa = ComputeGPA(note_repo, student_repo).execute("202504039")
print(f"GPA: {gpa}")   # (85 + 72 + 45) / 3 = 67.33