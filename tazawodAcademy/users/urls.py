from django.urls import path
from .views import RegisterStudentView

urlpatterns = [
    path(
        "student/register/",
        RegisterStudentView.as_view(),
        name="student register"
    )
]
