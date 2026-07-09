

#Domain Entity: Course

#Represents an academic course within the domain. Like Student, this
#class is fully independent of persistence, transport, or presentation
#concerns — it exists purely to encode what a Course *is* and what
#constraints define a valid one.


from dataclasses import dataclass


class InvalidCourseError(Exception):
    """
    Domain-specific exception.

    A dedicated exception type allows upper layers to distinguish
    a course-related business rule violation from unrelated
    technical errors, improving error handling specificity.
    """
    pass


@dataclass(frozen=True)
class Course:
    """
    Represents a course offered within the institution.

    frozen=True enforces immutability: once a Course is instantiated,
    its attributes cannot be reassigned. This prevents accidental
    mutation of course data (e.g., credit value) elsewhere in the
    system, preserving referential consistency wherever this Course
    instance is used — notably in GPA computation.
    """

    id: str
    name: str
    credits: int

    def __post_init__(self):
        """
        Validates business invariants immediately upon construction,
        ensuring no Course instance can exist in an invalid state.
        """

        # Rule 1: a course must have a stable identifier, since it
        # is referenced by Note entities to associate a grade with
        # a specific course.
        if not self.id:
            raise InvalidCourseError("Id cannot be empty.")

        # Rule 2: a course without a name has no meaningful identity
        # from an academic or administrative standpoint.
        if not self.name:
            raise InvalidCourseError("Name cannot be empty.")

        # Rule 3: credits must be strictly positive. Credits are a
        # weighting factor used in GPA calculation; a zero or
        # negative value would produce a meaningless or undefined
        # weighted average downstream.
        if self.credits <= 0:
            raise InvalidCourseError("Credits must be greater than 0.")

    def has_id(self, course_id: str) -> bool:
        
       # Checks whether the given identifier matches this course's id.

        return self.id == course_id


# ----------------------------------------------------------------
# Usage example (manual verification only; belongs in a unit test
# in a fully structured project).
# ----------------------------------------------------------------
course = Course(id="C1", name="Mathématiques", credits=7)

print(course.name)           # Mathématiques
print(course.has_id("C1"))   # True
print(course.has_id("C2"))   # False
