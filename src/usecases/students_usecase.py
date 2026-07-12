# Application Layer: Student Use Cases
#
# This module defines all use cases related to the Student entity.



from entities.students import Student
from repository.students_repository import StudentRepository


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

    Simple query use case — no side effects, no business rules
    beyond existence checking.
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