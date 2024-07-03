from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import QuraanDays, StudentData
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
        
class HomePageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == "student":
            student_data = StudentData.objects.get(student=user)
            quraan_days = QuraanDays.objects.filter(student=student_data)
            quraan_days_list = []
            for date in quraan_days:
                quraan_days_list.append({"day":date.day, "starts":date.starts, "delay": date.delay})
            return Response({
                "name": user.name,
                "userType": "student",
                "subscribed": student_data.subscribed,
                "quraan_days": quraan_days_list,
                "notes": []
            })
