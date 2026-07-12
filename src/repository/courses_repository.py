# Repository Interface: CourseRepository



from abc import ABC, abstractmethod
from typing import Optional

from entities.courses import Course


class CourseRepository(ABC):
    """
    Abstract interface for Course persistence.

    This is a port in Clean Architecture terms. It defines WHAT
    operations are available on Course storage, without saying
    HOW they are implemented.

    Concrete implementations live in the infrastructure layer
    and are injected into use cases at runtime.
    """

    @abstractmethod
    def save(self, course: Course) -> None:
        """
        Persist a new course or update an existing one.

        Args:
            course: a valid Course domain entity to store.
        """
        pass

    @abstractmethod
    def find_by_id(self, course_id: str) -> Optional[Course]:
        """
        Return a Course by its unique identifier.

        Args:
            course_id: the id to search for.

        Returns:
            The matching Course instance, or None if not found.
        """
        pass

    @abstractmethod
    def exists(self, course_id: str) -> bool:
        """
        Check whether a course with the given id already exists.

        Args:
            course_id: the id to check.

        Returns:
            True if a course with that id exists, False otherwise.
        """
        pass