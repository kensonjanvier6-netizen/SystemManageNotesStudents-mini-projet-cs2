# Repository Interface: StudentRepository
#
# This module defines the abstract interface (port) for Student
# persistence.

from abc import ABC, abstractmethod
from typing import Optional

from entities.students import Student


class StudentRepository(ABC):
    """
    Abstract interface for Student persistence.

    This is a port in Clean Architecture terms. It defines WHAT
    operations are available on Student storage, without saying
    HOW they are implemented.

    Concrete implementations live in the infrastructure layer
    and are injected into use cases at runtime.
    """

    @abstractmethod
    def save(self, student: Student) -> None:
        """
        Persist a new student or update an existing one.

        Args:
            student: a valid Student domain entity to store.
        """
        pass

    @abstractmethod
    def find_by_id(self, student_id: str) -> Optional[Student]:
        """
        Return a Student by its unique identifier.

        Args:
            student_id: the id to search for.

        Returns:
            The matching Student instance, or None if not found.
        """
        pass

    @abstractmethod
    def find_by_matricule(self, matricule: str) -> Optional[Student]:
        """
        Return a Student by its institutional matricule.

        Args:
            matricule: the matricule to search for.

        Returns:
            The matching Student instance, or None if not found.
        """
        pass

    @abstractmethod
    def exists(self, student_id: str) -> bool:
        """
        Check whether a student with the given id already exists.

        Args:
            student_id: the id to check.

        Returns:
            True if a student with that id exists, False otherwise.
        """
        pass