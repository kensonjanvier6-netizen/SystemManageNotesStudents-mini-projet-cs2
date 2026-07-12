# Interface Adapter: Note URLs + Dependency Injection
#
# This module wires everything together for the Note adapter:
# - Instantiates the repositories
# - Injects them into the use cases
# - Injects the use cases into the controllers
# - Declares the URL patterns


from django.urls import path
from use_cases.note_use_cases import AssignNote, GetStudentNotes, ComputeGPA
from infrastructure.note_repository_impl import InMemoryNoteRepository
from infrastructure.student_repository_impl import InMemoryStudentRepository
from infrastructure.course_repository_impl import InMemoryCourseRepository
from interface_adapters.note.controllers import (
    NoteListController,
    StudentNotesController,
    StudentGPAController,
)


# ================================================================
# DEPENDENCY INJECTION
# ================================================================

_note_repo    = InMemoryNoteRepository()
_student_repo = InMemoryStudentRepository()
_course_repo  = InMemoryCourseRepository()

_assign_note       = AssignNote(_note_repo, _student_repo, _course_repo)
_get_student_notes = GetStudentNotes(_note_repo, _student_repo)
_compute_gpa       = ComputeGPA(_note_repo, _student_repo)


# ================================================================
# URL PATTERNS
# ================================================================

urlpatterns = [
    path(
        "notes/",
        NoteListController.as_view(assign_note=_assign_note),
        name="note-list",
    ),
    path(
        "students/<str:student_id>/notes/",
        StudentNotesController.as_view(get_student_notes=_get_student_notes),
        name="student-notes",
    ),
    path(
        "students/<str:student_id>/gpa/",
        StudentGPAController.as_view(compute_gpa=_compute_gpa),
        name="student-gpa",
    ),
]


# ================================================================
# Include in your main urls.py like this:
# ================================================================
#
# from django.urls import path, include
#
# urlpatterns = [
#     path("api/", include("interface_adapters.student.urls")),
#     path("api/", include("interface_adapters.course.urls")),
#     path("api/", include("interface_adapters.note.urls")),
# ]
#
# Endpoints available:
#   POST   /api/notes/                        → assign a note
#   GET    /api/students/<id>/notes/          → get all notes for a student
#   GET    /api/students/<id>/gpa/            → get GPA for a student