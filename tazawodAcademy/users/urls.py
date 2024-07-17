from django.urls import path
from .views import RegisterStudentView, RegisterTeacherView, RegisterAdminView, LoginView

urlpatterns = [
    path(
        "student/register/",
        RegisterStudentView.as_view(),
        name="student register"
    ),
    path(
        "teacher/register/",
        RegisterTeacherView.as_view(),
        name="teacher register"
    ),
    path(
        "admin/register/",
        RegisterAdminView.as_view(),
        name="teacher register"
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login"
    )
]
