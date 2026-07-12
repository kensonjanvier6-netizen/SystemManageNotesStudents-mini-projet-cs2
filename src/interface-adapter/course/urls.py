# Interface Adapter: Course URLs + Dependency Injection
#
# This module wires everything together for the Course adapter:
# - Instantiates the repository
# - Injects it into the use cases
# - Injects the use cases into the controllers
# - Declares the URL patterns


from django.urls import path
from use_cases.course_use_cases import CreateCourse, GetCourse
from infrastructure.course_repository_impl import InMemoryCourseRepository
from interface_adapters.course.controllers import (
    CourseListController,
    CourseDetailController,
)


# ================================================================
# DEPENDENCY INJECTION
# ================================================================

_repository   = InMemoryCourseRepository()
_create_course = CreateCourse(_repository)
_get_course    = GetCourse(_repository)


# ================================================================
# URL PATTERNS
# ================================================================

urlpatterns = [
    path(
        "courses/",
        CourseListController.as_view(create_course=_create_course),
        name="course-list",
    ),
    path(
        "courses/<str:course_id>/",
        CourseDetailController.as_view(get_course=_get_course),
        name="course-detail",
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
# ]
#
# Endpoints available:
#   POST   /api/courses/             → create a course
#   GET    /api/courses/<id>/        → get a course by id