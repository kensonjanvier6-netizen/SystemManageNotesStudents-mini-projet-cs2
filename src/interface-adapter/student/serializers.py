# Interface Adapter: Student Serializer
#
# Serializers are responsible for converting raw HTTP request data
# into structured Python dicts, and converting domain entities into
# JSON-serializable dicts for HTTP responses.
#
# They act as a translation layer between the HTTP world and the
# domain/use case world — keeping both sides clean and independent.


# ================================================================
# INPUT SERIALIZER — validates incoming request data
# ================================================================

class CreateStudentInputSerializer:
    """
    Validates and structures the data received from an HTTP POST
    request to create a new student.

    Responsibilities:
    - Check that all required fields are present.
    - Check that no field is empty or blank.
    - Return clean, typed data ready for the use case.
    """

    REQUIRED_FIELDS = ["id", "matricule", "name"]

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
            if not value or not str(value).strip():
                self._errors[field] = f"'{field}' is required and cannot be empty."
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

class StudentOutputSerializer:
    """
    Converts a Student domain entity into a JSON-serializable dict
    for inclusion in an HTTP response.

    The domain entity must never be exposed directly to the HTTP
    layer — this serializer acts as a controlled output boundary.
    """

    @staticmethod
    def serialize(student) -> dict:
        """
        Converts a Student instance to a response dict.

        Args:
            student: a Student domain entity instance.

        Returns:
            A dict safe for JSON serialization.
        """
        return {
            "id":        student.id,
            "matricule": student.matricule,
            "name":      student.full_name(),
        }