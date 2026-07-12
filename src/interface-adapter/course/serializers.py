# Interface Adapter: Course Serializer
#
# Responsible for converting raw HTTP request data into structured
# Python dicts, and converting Course domain entities into
# JSON-serializable dicts for HTTP responses.


# ================================================================
# INPUT SERIALIZER — validates incoming request data
# ================================================================

class CreateCourseInputSerializer:
    """
    Validates and structures the data received from an HTTP POST
    request to create a new course.
    """

    REQUIRED_FIELDS = ["id", "name", "credits"]

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

            # Rule 2: credits must be a positive integer
            if field == "credits":
                try:
                    credits = int(value)
                    if credits <= 0:
                        self._errors[field] = "'credits' must be greater than 0."
                    else:
                        self._clean[field] = credits
                except (ValueError, TypeError):
                    self._errors[field] = "'credits' must be a valid integer."
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

class CourseOutputSerializer:
    """
    Converts a Course domain entity into a JSON-serializable dict
    for inclusion in an HTTP response.
    """

    @staticmethod
    def serialize(course) -> dict:
        """
        Converts a Course instance to a response dict.

        Args:
            course: a Course domain entity instance.

        Returns:
            A dict safe for JSON serialization.
        """
        return {
            "id":      course.id,
            "name":    course.name,
            "credits": course.credits,
        }