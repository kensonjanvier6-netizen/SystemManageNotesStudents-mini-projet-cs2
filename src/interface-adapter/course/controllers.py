# Interface Adapter: Course Controller
#
# Controllers receive HTTP requests, delegate to the appropriate
# use case, and return HTTP responses. No business logic here.


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from use_cases.course_use_cases import CreateCourse, GetCourse
from entities.course import InvalidCourseError
from interface_adapters.course.serializers import (
    CreateCourseInputSerializer,
    CourseOutputSerializer,
)


@method_decorator(csrf_exempt, name="dispatch")
class CourseListController(View):
    """
    Handles HTTP requests for the /courses/ endpoint.

    POST /courses/ — create a new course.
    """

    def __init__(self, create_course: CreateCourse, **kwargs):
        super().__init__(**kwargs)
        self._create_course = create_course

    def post(self, request):
        """
        Creates a new course from JSON request body.

        Expected body:
            {
                "id":      "C1",
                "name":    "Mathematiques",
                "credits": 7
            }

        Returns:
            201 Created     — with the new course data.
            400 Bad Request — if validation fails.
            409 Conflict    — if a course with that id already exists.
        """

        # Step 1: parse the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

        # Step 2: validate input
        serializer = CreateCourseInputSerializer(data)
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        # Step 3: execute the use case
        try:
            course = self._create_course.execute(
                course_id=serializer.validated_data["id"],
                name=serializer.validated_data["name"],
                credits=serializer.validated_data["credits"],
            )
        except InvalidCourseError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=409)

        # Step 4: serialize and return the response
        return JsonResponse(CourseOutputSerializer.serialize(course), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CourseDetailController(View):
    """
    Handles HTTP requests for the /courses/<course_id>/ endpoint.

    GET /courses/<course_id>/ — retrieve a course by id.
    """

    def __init__(self, get_course: GetCourse, **kwargs):
        super().__init__(**kwargs)
        self._get_course = get_course

    def get(self, request, course_id: str):
        """
        Retrieves a course by its id.

        Returns:
            200 OK        — with the course data.
            404 Not Found — if no course with that id exists.
        """

        # Step 1: execute the use case
        try:
            course = self._get_course.execute(course_id)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=404)

        # Step 2: serialize and return the response
        return JsonResponse(CourseOutputSerializer.serialize(course), status=200)