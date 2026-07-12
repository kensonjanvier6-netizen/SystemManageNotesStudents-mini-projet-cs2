# Interface Adapter: Note Serializer
#
# Responsible for converting raw HTTP request data into structured
# Python dicts, and converting Note domain entities into
# JSON-serializable dicts for HTTP responses.


# ================================================================
# INPUT SERIALIZER — validates incoming request data
# ================================================================

class AssignNoteInputSerializer:
    """
    Validates and structures the data received from an HTTP POST
    request to assign a grade to a student for a course.
    """

    REQUIRED_FIELDS = ["id", "student_id", "course_id", "value"]

    def __init__(self, data: dict):
        self._data   = data
        self._errors = {}
        self._clean  = {}

    def is_valid(self) -> bool:
        """
        Runs all validation checks.

        Returns:
            True if data is valid, False otherwise.
        """
        self._errors = {}
        self._clean  = {}

        for field in self.REQUIRED_FIELDS:
            value = self._data.get(field, "")

            # Rule 1: field must be present and not empty
            if value == "" or value is None:
                self._errors[field] = f"'{field}' is required and cannot be empty."
                continue

            # Rule 2: value must be a number between 0 and 100
            if field == "value":
                try:
                    note_value = float(value)
                    if not (0 <= note_value <= 100):
                        self._errors[field] = "'value' must be between 0 and 100."
                    else:
                        self._clean[field] = note_value
                except (ValueError, TypeError):
                    self._errors[field] = "'value' must be a valid number."
            else:
                self._clean[field] = str(value).strip()

        return len(self._errors) == 0

    @property
    def errors(self) -> dict:
        """Returns validation errors, keyed by field name."""
        return self._errors

    @property
    def validated_data(self) -> dict:
        """Returns clean validated data, ready for the use case."""
        return self._clean


# ================================================================
# OUTPUT SERIALIZER — formats domain entity for HTTP response
# ================================================================

class NoteOutputSerializer:
    """
    Converts a Note domain entity into a JSON-serializable dict
    for inclusion in an HTTP response.
    """

    @staticmethod
    def serialize(note) -> dict:
        """
        Converts a Note instance to a response dict.

        Args:
            note: a Note domain entity instance.

        Returns:
            A dict safe for JSON serialization.
        """
        return {
            "id":         note.id,
            "student_id": note.student_id,
            "course_id":  note.course_id,
            "value":      note.value,
            "mention":    note.mention(),
            "is_passing": note.is_passing(),
        }

    @staticmethod
    def serialize_many(notes: list) -> list:
        """
        Converts a list of Note instances to a list of dicts.

        Args:
            notes: a list of Note domain entity instances.

        Returns:
            A list of dicts safe for JSON serialization.
        """
        return [NoteOutputSerializer.serialize(note) for note in notes]