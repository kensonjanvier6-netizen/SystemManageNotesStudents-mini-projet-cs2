# Repository Interface: NoteRepository


from abc import ABC, abstractmethod
from typing import Optional

from entities.notes import Note


class NoteRepository(ABC):
    """
    Abstract interface for Note persistence.

    This is a port in Clean Architecture terms. It defines WHAT
    operations are available on Note storage, without saying
    HOW they are implemented.

    Concrete implementations live in the infrastructure layer
    and are injected into use cases at runtime.
    """

    @abstractmethod
    def save(self, note: Note) -> None:
        """
        Persist a new note or update an existing one.

        Args:
            note: a valid Note domain entity to store.
        """
        pass

    @abstractmethod
    def find_by_id(self, note_id: str) -> Optional[Note]:
        """
        Return a Note by its unique identifier.

        Args:
            note_id: the id to search for.

        Returns:
            The matching Note instance, or None if not found.
        """
        pass

    @abstractmethod
    def find_by_student(self, student_id: str) -> list[Note]:
        """
        Return all notes belonging to a given student.

        Args:
            student_id: the student id to filter by.

        Returns:
            A list of Note instances (may be empty).
        """
        pass

    @abstractmethod
    def exists(self, note_id: str) -> bool:
        """
        Check whether a note with the given id already exists.

        Args:
            note_id: the id to check.

        Returns:
            True if a note with that id exists, False otherwise.
        """
        pass