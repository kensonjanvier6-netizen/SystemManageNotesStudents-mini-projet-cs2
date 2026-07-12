# Application Layer: Course Use Cases



from entities.courses import Course
from repositories.course_repository import CourseRepository


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