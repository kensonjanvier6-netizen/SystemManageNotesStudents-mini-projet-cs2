# Application Layer: Student Use Cases
#
# This module defines the Repository interface (port) and all
# use cases related to the Student entity. Use cases orchestrate
# domain logic without depending on any framework, database, or
# external tool — they only depend on the domain entities and
# the repository abstraction defined here.

from abc import ABC, abstractmethod
from typing import Optional
from domain.student import Student, InvalidStudentError


# ================================================================
# REPOSITORY INTERFACE (Port)
# ================================================================

class StudentRepository(ABC):
    """
    Abstract interface for Student persistence.

    This is a port in Clean Architecture terms. The actual
    implementation (InMemoryStudentRepository, DjangoStudentRepository,
    etc.) lives in the outer layer and is injected at runtime.
    The use cases never know which implementation is being used.
    """

    @abstractmethod
    def save(self, student: Student) -> None:
        """Persist a new student or update an existing one."""
        pass

    @abstractmethod
    def find_by_id(self, student_id: str) -> Optional[Student]:
        """Return a Student by its id, or None if not found."""
        pass

    @abstractmethod
    def find_by_matricule(self, matricule: str) -> Optional[Student]:
        """Return a Student by its matricule, or None if not found."""
        pass

    @abstractmethod
    def exists(self, student_id: str) -> bool:
        """Return True if a student with the given id already exists."""
        pass


# ================================================================
# USE CASE 1: CreateStudent
# ================================================================

class CreateStudent:
    """
    Use case: register a new student in the system.

    Business rules enforced here:
    - A student with the same id must not already exist.
    - A student with the same matricule must not already exist.
    - All field validations are delegated to the Student entity.
    """

    def __init__(self, repository: StudentRepository):
        self._repository = repository

    def execute(self, student_id: str, matricule: str, name: str) -> Student:
        """
        Creates and persists a new Student.

        Args:
            student_id: unique identifier for the student.
            matricule:  official institutional identifier.
            name:       full name of the student.

        Returns:
            The newly created Student instance.

        Raises:
            InvalidStudentError: if any field is invalid.
            ValueError: if a student with the same id or matricule exists.
        """

        # Rule 1: no duplicate id
        if self._repository.exists(student_id):
            raise ValueError(f"A student with id '{student_id}' already exists.")

        # Rule 2: no duplicate matricule
        if self._repository.find_by_matricule(matricule) is not None:
            raise ValueError(f"A student with matricule '{matricule}' already exists.")

        # Delegate field validation to the domain entity
        student = Student(id=student_id, matricule=matricule, name=name)

        self._repository.save(student)
        return student


# ================================================================
# USE CASE 2: GetStudent
# ================================================================

class GetStudent:
    """
    Use case: retrieve a student by their id.

    This use case is a simple query — it carries no side effects
    and enforces no business rule beyond existence checking.
    """

    def __init__(self, repository: StudentRepository):
        self._repository = repository

    def execute(self, student_id: str) -> Student:
        """
        Retrieves a Student by id.

        Args:
            student_id: the unique identifier of the student.

        Returns:
            The matching Student instance.

        Raises:
            ValueError: if no student with that id is found.
        """

        student = self._repository.find_by_id(student_id)

        if student is None:
            raise ValueError(f"No student found with id '{student_id}'.")

        return student


# ================================================================
# IN-MEMORY IMPLEMENTATION (for testing / manual verification)
# ================================================================

class InMemoryStudentRepository(StudentRepository):
    """
    Simple in-memory implementation of StudentRepository.

    Used for unit testing and manual verification only.
    In a real project, this would be replaced by a Django ORM
    or any other persistence adapter in the outer layer.
    """

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


# ================================================================
# Usage example
# ================================================================

repo = InMemoryStudentRepository()
create = CreateStudent(repo)
get    = GetStudent(repo)

student = create.execute(
    student_id="202504039",
    matricule="MAT141",
    name="Kenson Janvier"
)

print(student.full_name())   # Kenson Janvier

found = get.execute("202504039")
print(found.matricule)       # MAT141
