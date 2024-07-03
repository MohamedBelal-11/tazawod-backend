from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import AllowAny
from .models import StudentData
from .serializers import UserSerializer, QuraanDaysSerializer
from django.contrib.auth import authenticate, login
from string import ascii_letters, digits
# import random
from twilio.rest import Client # type: ignore

# account_sid = 'AC91a909b98c7035d13ace54504bc8c1ab'
# auth_token = 'ee551801f23a4a05c98b9063b20e35d3'
# client = Client(account_sid, auth_token)

# def send_message(phone_number, otp):
#     message = client.messages.create(
#         from_='whatsapp:+14155238886',
#         body=f'كود التحقق الخاص بك هو {otp}',
#         to=f'whatsapp:+{phone_number}'
#     )
#     return message

# def num_hours(time: str):
#     if len(time) > 8 or len(time) < 7:
#         raise ValueError()
#     rtime = time[:-3]
#     return float(rtime[:-3]) + (float(rtime[-2:]) / 60)

def is_valid_time_format(time_string):
    try:
        # Try to parse the time string
        datetime.strptime(time_string, '%H:%M:%S')
        return True
    except ValueError:
        # If parsing fails, the format is incorrect
        return False

marksList = ['!', '@', '#', '$', '%', '^', '&', '*', '?', '_', '-']
arCharsList = [
    'ض',
    'ص',
    'ث',
    'ق',
    'ف',
    'غ',
    'إ',
    'ع',
    'ه',
    'خ',
    'ح',
    'ج',
    'د',
    'ش',
    'س',
    'ي',
    'ب',
    'ل',
    'ا',
    'أ',
    'ت',
    'ن',
    'م',
    'ك',
    'ط',
    'ئ',
    'ء',
    'ؤ',
    'ر',
    'آ',
    'ة',
    'و',
    'ز',
    'ظ',
];


class RegisterStudentView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        data: dict = request.data
        data["user_type"] = "student"
        student_serializer = UserSerializer(data=data)
        quraan_days = data.get("quraan_days", [])

        name: str = data.get("name",  None)
        if name.endswith(" ") or name.startswith(" ") or ("  " in name):
            return Response("name not valid",status=status.HTTP_400_BAD_REQUEST)

        for c in name:
            if not c in [*ascii_letters, *arCharsList, " "]:
                return Response("name not valid 2",status=status.HTTP_400_BAD_REQUEST)

        password: str = data.get("password", None)

        if len(password) < 8:
            return Response("password is short",status=status.HTTP_400_BAD_REQUEST)
            

        for c in password:
            if not c in [*ascii_letters, *digits, *marksList]:
                return Response("password not valid", status=status.HTTP_400_BAD_REQUEST)

        alive2 = False
        for c in password:
            if c in ascii_letters:
                alive2 = True
                break

        if not alive2:
            return Response("password needs chars", status=status.HTTP_400_BAD_REQUEST)

        alive2 = False
        for c in password:
            if c in marksList:
                alive2 = True
                break

        if not alive2:
            return Response("password needs marks", status=status.HTTP_400_BAD_REQUEST)

        alive2 = False
        for c in password:
            if c in digits:
                alive2 = True
                break

        if not alive2:
            return Response("password not valid", status=status.HTTP_400_BAD_REQUEST)

        # tmplist = []
        for date_list in [quraan_days]:
            # Checking if the date list  
            if (len(date_list) == 0) or (len(date_list) > 7):
                return Response("there is no quraan_days",status=status.HTTP_400_BAD_REQUEST)
            for date in date_list:
                if not date["day"] in ["sunday", "monday", "tuesday", "wednesday", "thurusday", "friday", "saturday"]:
                    return Response("there is no valid day",status=status.HTTP_400_BAD_REQUEST)
                if (not is_valid_time_format(date["starts"])) or (not is_valid_time_format(date["starts"])):
                    return Response("the time isn't valid",status=status.HTTP_400_BAD_REQUEST)
        #         for date_num in tmplist:
        #             if (
        #                 (num_hours(date["starts"]) > date_num[0] and
        #                 num_hours(date["starts"]) < date_num[1] and
        #                 date["day"] == date_num[2]) or
        #                 (num_hours(date["starts"]) + num_hours(date["delay"]) > date_num[0] and
        #                 num_hours(date["starts"]) + num_hours(date["delay"]) < date_num[1] and
        #                 date["day"] == date_num[2]) or
        #                 (date_num[0] > num_hours(date["starts"]) and
        #                 date_num[0] < num_hours(date["starts"]) + num_hours(date["delay"]) and
        #                 date["day"] == date_num[2]) or
        #                 (date_num[1] > num_hours(date["starts"]) and
        #                 date_num[1] < num_hours(date["starts"]) + num_hours(date["delay"]) and
        #                 date["day"] == date_num[2]) or
        #                 (num_hours(date["starts"]) == date_num[0] and
        #                 num_hours(date["starts"]) + num_hours(date["delay"]) == date_num[1] and
        #                 date["day"] == date_num[2])
        #             ):
        #                 return Response(status=status.HTTP_400_BAD_REQUEST)
        #             tmplist.append([
        #                 num_hours(date["starts"]),
        #                 num_hours(date["starts"]) + num_hours(date["delay"]),
        #                 date["day"],
        #             ])

        for dates_list in [quraan_days]:
            tmp_list = []
            for date in dates_list:
                if (
                    (not (date["starts"][-5:-3] == "00" or date["starts"][-5:-3] == "30")) or
                    (not (date["delay"][-5:-3] == "00" or date["delay"][-5:-3] == "30")) or
                    (not (int(date["delay"][:-6]) < 4 and int(date["delay"][:-6]) > -1)) or
                    date["delay"] == "0:00:00" or
                    date["delay"] == "3:30:00"
                ):
                    return Response("error on starts or delay",status=status.HTTP_400_BAD_REQUEST)
                for day in tmp_list:
                    if date["day"] == day:
                        return Response("there are two same days", status=status.HTTP_400_BAD_REQUEST)
                tmp_list.append(date["day"])

        if student_serializer.is_valid():
            student = student_serializer.save()
            student_data = StudentData.objects.create(student=student)
            user = authenticate(username=student.username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)

            else:
                print("Authentication failed")
                return Response({"success": False, "message": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST)
            # phone_number = student.phone_number
            # otp = random.randint(1000, 9999)  # Generate a random OTP
            # student.otp = otp
            # student.save()
            # send_message(phone_number, otp)
            
            # # Store the password in the session securely
            # request.session['temp_verify'] = {
            #     "password":request.data.get('password'),
            #     "phone": phone_number
            # }

            errors = []
            for date_data in quraan_days:
                date_data['student'] = student_data.id
                date_serializer = QuraanDaysSerializer(data=date_data)
                if date_serializer.is_valid():
                    date_serializer.save()
                else:
                    errors.append(date_serializer.errors)

            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": True, "token": token.key}, status=status.HTTP_201_CREATED)
        
        return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VerifyOTPView(APIView):
#     def post(self, request):
#         phone_number = request.data.get('phone_number')
#         otp = request.data.get('otp')
#         try:
#             student = Student.objects.get(phone_number=phone_number)
#             if student.otp == int(otp):
#                 student.is_verified = True
#                 student.otp = None  # Clear the OTP after verification
#                 student.save()
#                 # Retrieve the password from the session
#                 temp_verify = request.session.pop('temp_password', None)
#                 if temp_verify is None:
#                     return Response({"success": False, "message": "Password not found in session"}, status=status.HTTP_400_BAD_REQUEST)
#                 password = temp_verify.pop('password', None)
#                 if password is None:
#                     return Response({"success": False, "message": "Password not found in session"}, status=status.HTTP_400_BAD_REQUEST)
#                 # Authenticate and log in the user
#                 student = authenticate(username=student.username, password=password)
#                 if student:
#                     login(request, student)
                    
#                     # Generate token if using TokenAuthentication
#                     token, _ = Token.objects.get_or_create(user=student)
                    
#                     return Response({"success": True, "token": token.key}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"success": False, "message": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({"success": False, "message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
#         except Student.DoesNotExist:
#             return Response({"success": False, "message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)