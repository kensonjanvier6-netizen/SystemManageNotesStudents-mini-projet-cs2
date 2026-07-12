# Interface Adapter: Student URLs + Dependency Injection
#
# This module wires everything together:
# - Instantiates the repository
# - Injects it into the use cases
# - Injects the use cases into the controllers
# - Declares the URL patterns
#
# This is the only place where concrete implementations are named.
# All other layers depend only on abstractions.


from django.urls import path
from use_cases.student_use_cases import (
    CreateStudent,
    GetStudent,
    InMemoryStudentRepository,
)
from interface_adapters.student.controllers import (
    StudentListController,
    StudentDetailController,
)


# ================================================================
# DEPENDENCY INJECTION
# ================================================================

# In a real Django project, you would replace InMemoryStudentRepository
# with a DjangoStudentRepository (using Django ORM models).
# Only this file needs to change — all other layers stay untouched.

_repository    = InMemoryStudentRepository()
_create_student = CreateStudent(_repository)
_get_student    = GetStudent(_repository)


# ================================================================
# URL PATTERNS
# ================================================================

urlpatterns = [
    path(
        "students/",
        StudentListController.as_view(create_student=_create_student),
        name="student-list",
    ),
    path(
        "students/<str:student_id>/",
        StudentDetailController.as_view(get_student=_get_student),
        name="student-detail",
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
# ]
#
# Endpoints available:
#   POST   /api/students/             → create a student
#   GET    /api/students/<id>/        → get a student by id