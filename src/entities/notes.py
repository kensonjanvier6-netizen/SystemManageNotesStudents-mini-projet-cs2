# Domain Entity: Note


from dataclasses import dataclass


class InvalidNoteError(Exception):
    """
    Domain-specific exception.

    A dedicated exception type allows upper layers to distinguish
    a grade-related business rule violation from unrelated
    technical errors, improving error handling specificity.
    """
    pass


@dataclass(frozen=True)
class Note:
    """
    Represents a grade assigned to a student for a given course.

    frozen=True enforces immutability: once a Note is instantiated,
    its attributes cannot be reassigned. This prevents accidental
    mutation of grade data elsewhere in the system, preserving
    referential consistency — notably during GPA computation or
    mention evaluation.
    """

    id: str
    student_id: str
    course_id: str
    value: float

    def __post_init__(self):
        """
        Validates business invariants immediately upon construction,
        ensuring no Note instance can exist in an invalid state.
        """

        # Rule 1: a note must have a stable identifier, used to
        # uniquely reference this grade record within the domain.
        if not self.id:
            raise InvalidNoteError("Id cannot be empty.")

        # Rule 2: a note must be linked to a student. Without this
        # reference, the grade has no academic subject to belong to.
        if not self.student_id:
            raise InvalidNoteError("Student id cannot be empty.")

        # Rule 3: a note must be linked to a course. Without this
        # reference, the grade carries no academic context or
        # credit weighting for GPA computation.
        if not self.course_id:
            raise InvalidNoteError("Course id cannot be empty.")

        # Rule 4: the grade value must be within the valid academic
        # range of 0 to 100. A value outside this range has no
        # meaningful interpretation within this domain.
        if not (0 <= self.value <= 100):
            raise InvalidNoteError("Value must be between 0 and 100.")

    def is_passing(self) -> bool:
        """
        Returns True if the grade meets the passing threshold.

        The passing threshold is set at 60. Any value below 60
        is considered a failure within this academic domain.
        """
        return self.value >= 60

    def mention(self) -> str:
        """
        Returns the academic mention corresponding to the grade value.

        Mention scale:
          - 0  to 59  → Failure  (below passing threshold)
          - 60 to 79  → Good     (satisfactory academic performance)
          - 80 to 100 → Perfect  (outstanding academic performance)
        """
        if self.value < 60:
            return "Failure"
        elif self.value < 80:
            return "Good"
        else:
            return "Perfect"

    def belongs_to_student(self, student_id: str) -> bool:
        """
        Checks whether this note belongs to the given student.
        """
        return self.student_id == student_id

    def belongs_to_course(self, course_id: str) -> bool:
        """
        Checks whether this note is associated with the given course.
        """
        return self.course_id == course_id


# ----------------------------------------------------------------
# Usage example (manual verification only; belongs in a unit test
# in a fully structured project).
# ----------------------------------------------------------------
note1 = Note(id="N1", student_id="202504039", course_id="C141", value=85)
note3 = Note(id="N3", student_id="202504039", course_id="C100", value=45)

print(note1.mention())                        # Perfect
print(note3.mention())                        # Failure

print(note1.is_passing())                     # True
print(note3.is_passing())                     # False

print(note1.belongs_to_student("202504039"))  # True
print(note1.belongs_to_course("C141"))          # True