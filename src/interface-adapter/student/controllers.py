# Interface Adapter: Student Controller
#
# Controllers receive HTTP requests, delegate to the appropriate
# use case, and return HTTP responses. They never contain business
# logic — they only orchestrate the flow between HTTP and use cases.


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from use_cases.student_use_cases import CreateStudent, GetStudent
from domain.student import InvalidStudentError
from interface_adapters.student.serializers import (
    CreateStudentInputSerializer,
    StudentOutputSerializer,
)


@method_decorator(csrf_exempt, name="dispatch")
class StudentListController(View):
    """
    Handles HTTP requests for the /students/ endpoint.

    POST /students/ — create a new student.
    """

    def __init__(self, create_student: CreateStudent, **kwargs):
        super().__init__(**kwargs)
        self._create_student = create_student

    def post(self, request):
        """
        Creates a new student from JSON request body.

        Expected body:
            {
                "id":        "202504039",
                "matricule": "MAT141",
                "name":      "Kenson Janvier"
            }

        Returns:
            201 Created  — with the new student data.
            400 Bad Request — if validation fails.
        """

        # Step 1: parse the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

        # Step 2: validate input
        serializer = CreateStudentInputSerializer(data)
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        # Step 3: execute the use case
        try:
            student = self._create_student.execute(
                student_id=serializer.validated_data["id"],
                matricule=serializer.validated_data["matricule"],
                name=serializer.validated_data["name"],
            )
        except InvalidStudentError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=409)

        # Step 4: serialize and return the response
        return JsonResponse(StudentOutputSerializer.serialize(student), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class StudentDetailController(View):
    """
    Handles HTTP requests for the /students/<student_id>/ endpoint.

    GET /students/<student_id>/ — retrieve a student by id.
    """

    def __init__(self, get_student: GetStudent, **kwargs):
        super().__init__(**kwargs)
        self._get_student = get_student

    def get(self, request, student_id: str):
        """
        Retrieves a student by their id.

        Returns:
            200 OK        — with the student data.
            404 Not Found — if no student with that id exists.
        """

        # Step 1: execute the use case
        try:
            student = self._get_student.execute(student_id)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=404)

        # Step 2: serialize and return the response
        return JsonResponse(StudentOutputSerializer.serialize(student), status=200)