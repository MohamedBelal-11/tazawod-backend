from datetime import time, timedelta
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import QuraanDays, StudentData, TeacherData, AdminData, User
from rest_framework.views import APIView
from rest_framework import status
from .utils import get_weekday
from typing import List, TypedDict

class HomePageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, *args, **kwargs):
        # Get the authenticated user
        user = request.user

        if not isinstance(user, User):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # If the user is a student
        if user.user_type == "student":
            # Get the student data
            student_data = StudentData.objects.get(student=user)
            # Get the Quraan days for the student
            quraan_days = QuraanDays.objects.filter(student=student_data)
            # Convert the Quraan days to a list of dictionaries
            quraan_days_list = [{
                "day": date.day,
                "starts": date.starts,
                "delay": date.delay
            } for date in quraan_days]

            # Return the response
            return Response({
                "name": user.name,
                "userType": "student",
                "subscribed": student_data.subscribed,
                "quraan_days": quraan_days_list,
                "notes": []
            }, status=status.HTTP_200_OK)

        # If the user is a teacher
        if user.user_type == "teacher":
            # Get the teacher data
            teacher_data = TeacherData.objects.get(teacher=user)

            # If the teacher is accepted
            if teacher_data.is_accepted:
                # Get the students of the teacher
                teacher_students = StudentData.objects.filter(
                    teacher=teacher_data,
                    subscribed=True
                )

                # Initialize the today and tomorrow meetings lists
                class Meeting(TypedDict):
                    student: str
                    starts: time
                    delay: timedelta

                today_meetings: List[Meeting] = []
                tomorrow_meetings: List[Meeting] = []

                # For each student of the teacher
                for student in teacher_students:
                    # Get the Quraan days of the student for today
                    student_today_meeting = QuraanDays.objects.filter(
                        student=student,
                        day=get_weekday()
                    )

                    # Convert the Quraan days to a list of dictionaries
                    for date in student_today_meeting:
                        today_meetings.append({
                            "student": student.student.name,
                            "starts": date.starts,
                            "delay": date.delay
                        })

                    # Get the Quraan days of the student for tomorrow
                    student_tomorrow_meeting = QuraanDays.objects.filter(
                        student=student,
                        day=get_weekday(1)
                    )

                    # Convert the Quraan days to a list of dictionaries
                    for date in student_tomorrow_meeting:
                        tomorrow_meetings.append({
                            "student": student.student.name,
                            "starts": date.starts,
                            "delay": date.delay
                        })

                # Sort the today meetings by starting time
                sorted_today_meetings = sorted(
                    today_meetings,
                    key=lambda x: x['starts']
                )

                # Sort the tomorrow meetings by starting time
                sorted_tomorrow_meetings = sorted(
                    tomorrow_meetings,
                    key=lambda x: x['starts']
                )

                # Return the response
                return Response({
                    "name": user.name,
                    "userType": "teacher",
                    "is_accepted": True,
                    "today_meetings": sorted_today_meetings,
                    "tomorrow_meetings": sorted_tomorrow_meetings,
                    "notes": []
                },status=status.HTTP_200_OK)

            # If the teacher is not accepted
            # Get the super admins
            super_admins = User.objects.filter(user_type="superadmin")
            # Convert the super admins to a list of dictionaries
            super_admins_list = [{
                "name": admin.name,
                "phone": admin.phone_number
            } for admin in super_admins]

            # Return the response
            return Response({
                "name": user.name,
                "userType": "teacher",
                "is_accepted": False,
                "super_admins": super_admins_list
            }, status=status.HTTP_200_OK)

        # If the user is an admin
        if user.user_type == "admin":
            # Get the admin data
            admin_data = AdminData.objects.get(admin=user)

            # If the admin is accepted
            if admin_data.is_accepted:
                # Return the response
                return Response({
                    "name": user.name,
                    "userType": "admin",
                    "is_accepted": True,
                    "live_meetings": []
                }, status=status.HTTP_200_OK)

            # If the admin is not accepted
            # Get the super admins
            super_admins = User.objects.filter(user_type="superadmin")
            # Convert the super admins to a list of dictionaries
            super_admins_list = [{
                "name": admin.name,
                "phone": admin.phone_number
            } for admin in super_admins]

            # Return the response
            return Response({
                "name": user.name,
                "userType": "admin",
                "is_accepted": False,
                "super_admins": super_admins_list
            }, status=status.HTTP_200_OK)

        # If the user is a super admin
        if user.user_type == "superadmin":
            # Return the response
            return Response({
                "name": user.name,
                "userType": "superadmin",
                "live_meetings": []
            }, status=status.HTTP_200_OK)
