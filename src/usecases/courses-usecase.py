# Application Layer: Course Use Cases
#
# This module defines the Repository interface (port) and all
# use cases related to the Course entity.

from abc import ABC, abstractmethod
from typing import Optional
from domain.course import Course, InvalidCourseError


# ================================================================
# REPOSITORY INTERFACE (Port)
# ================================================================

class CourseRepository(ABC):
    """
    Abstract interface for Course persistence.

    The actual implementation lives in the outer layer and is
    injected at runtime. Use cases never depend on a concrete
    persistence mechanism.
    """

    @abstractmethod
    def save(self, course: Course) -> None:
        """Persist a new course or update an existing one."""
        pass

    @abstractmethod
    def find_by_id(self, course_id: str) -> Optional[Course]:
        """Return a Course by its id, or None if not found."""
        pass

    @abstractmethod
    def exists(self, course_id: str) -> bool:
        """Return True if a course with the given id already exists."""
        pass


# ================================================================
# USE CASE 1: CreateCourse
# ================================================================

class CreateCourse:
    """
    Use case: register a new course in the system.

    Business rules enforced here:
    - A course with the same id must not already exist.
    - All field validations are delegated to the Course entity.
    """

    def __init__(self, repository: CourseRepository):
        self._repository = repository

    def execute(self, course_id: str, name: str, credits: int) -> Course:
        """
        Creates and persists a new Course.

        Args:
            course_id: unique identifier for the course.
            name:      name of the course.
            credits:   credit value (must be greater than 0).

        Returns:
            The newly created Course instance.

        Raises:
            InvalidCourseError: if any field is invalid.
            ValueError: if a course with the same id already exists.
        """

        # Rule 1: no duplicate id
        if self._repository.exists(course_id):
            raise ValueError(f"A course with id '{course_id}' already exists.")

        # Delegate field validation to the domain entity
        course = Course(id=course_id, name=name, credits=credits)

        self._repository.save(course)
        return course


# ================================================================
# USE CASE 2: GetCourse
# ================================================================

class GetCourse:
    """
    Use case: retrieve a course by its id.

    Simple query use case — no side effects, no business rules
    beyond existence checking.
    """

    def __init__(self, repository: CourseRepository):
        self._repository = repository

    def execute(self, course_id: str) -> Course:
        """
        Retrieves a Course by id.

        Args:
            course_id: the unique identifier of the course.

        Returns:
            The matching Course instance.

        Raises:
            ValueError: if no course with that id is found.
        """

        course = self._repository.find_by_id(course_id)

        if course is None:
            raise ValueError(f"No course found with id '{course_id}'.")

        return course


# ================================================================
# IN-MEMORY IMPLEMENTATION (for testing / manual verification)
# ================================================================

class InMemoryCourseRepository(CourseRepository):
    """
    Simple in-memory implementation of CourseRepository.
    """

    def __init__(self):
        self._store: dict[str, Course] = {}

    def save(self, course: Course) -> None:
        self._store[course.id] = course

    def find_by_id(self, course_id: str) -> Optional[Course]:
        return self._store.get(course_id)

    def exists(self, course_id: str) -> bool:
        return course_id in self._store


# ================================================================
# Usage example
# ================================================================

repo   = InMemoryCourseRepository()
create = CreateCourse(repo)
get    = GetCourse(repo)

course = create.execute(course_id="C1", name="Mathematiques", credits=7)

print(course.name)          # Mathematiques
print(course.credits)       # 7

found = get.execute("C1")
print(found.has_id("C1"))   # True