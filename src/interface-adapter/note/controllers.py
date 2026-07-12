# Interface Adapter: Note Controller
#
# Controllers receive HTTP requests, delegate to the appropriate
# use case, and return HTTP responses. No business logic here.


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from use_cases.note_use_cases import AssignNote, GetStudentNotes, ComputeGPA
from interface_adapters.note.serializers import (
    AssignNoteInputSerializer,
    NoteOutputSerializer,
)


@method_decorator(csrf_exempt, name="dispatch")
class NoteListController(View):
    """
    Handles HTTP requests for the /notes/ endpoint.

    POST /notes/ — assign a grade to a student for a course.
    """

    def __init__(self, assign_note: AssignNote, **kwargs):
        super().__init__(**kwargs)
        self._assign_note = assign_note

    def post(self, request):
        """
        Assigns a grade from JSON request body.

        Expected body:
            {
                "id":         "N1",
                "student_id": "202504039",
                "course_id":  "C1",
                "value":      85
            }

        Returns:
            201 Created     — with the new note data.
            400 Bad Request — if validation fails.
            409 Conflict    — if a note with that id already exists.
        """

        # Step 1: parse the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

        # Step 2: validate input
        serializer = AssignNoteInputSerializer(data)
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        # Step 3: execute the use case
        try:
            note = self._assign_note.execute(
                note_id=serializer.validated_data["id"],
                student_id=serializer.validated_data["student_id"],
                course_id=serializer.validated_data["course_id"],
                value=serializer.validated_data["value"],
            )
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=409)

        # Step 4: serialize and return the response
        return JsonResponse(NoteOutputSerializer.serialize(note), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class StudentNotesController(View):
    """
    Handles HTTP requests for the /students/<student_id>/notes/ endpoint.

    GET /students/<student_id>/notes/ — retrieve all notes for a student.
    """

    def __init__(self, get_student_notes: GetStudentNotes, **kwargs):
        super().__init__(**kwargs)
        self._get_student_notes = get_student_notes

    def get(self, request, student_id: str):
        """
        Retrieves all notes for a given student.

        Returns:
            200 OK        — with the list of notes.
            404 Not Found — if no student with that id exists.
        """

        try:
            notes = self._get_student_notes.execute(student_id)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=404)

        return JsonResponse(
            {"student_id": student_id, "notes": NoteOutputSerializer.serialize_many(notes)},
            status=200,
        )


@method_decorator(csrf_exempt, name="dispatch")
class StudentGPAController(View):
    """
    Handles HTTP requests for the /students/<student_id>/gpa/ endpoint.

    GET /students/<student_id>/gpa/ — compute the GPA of a student.
    """

    def __init__(self, compute_gpa: ComputeGPA, **kwargs):
        super().__init__(**kwargs)
        self._compute_gpa = compute_gpa

    def get(self, request, student_id: str):
        """
        Computes and returns the GPA of a given student.

        Returns:
            200 OK        — with the GPA value.
            404 Not Found — if no student with that id exists.
        """

        try:
            gpa = self._compute_gpa.execute(student_id)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=404)

        return JsonResponse(
            {"student_id": student_id, "gpa": gpa},
            status=200,
        )