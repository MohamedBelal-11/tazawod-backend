from rest_framework import serializers
from .models import User, QuraanDays
from django.utils import timezone
import re


class QuraanDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuraanDays
        fields = ['id', 'day', 'starts', 'delay', 'student']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'phone_number',
            'password',
            'name',
            'gender',
            'user_type'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_phone_number(self, value):
        # Check if the phone number is unique
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        
        # Validate phone number format (adjust regex as needed)
        phone_regex = re.compile(r'^\d{9,15}$')
        if not phone_regex.match(value):
            raise serializers.ValidationError("Enter a valid phone number. The number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        
        return value

    def generate_unique_username(self, base_username):
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        return username

    def create(self, validated_data):
        base_username = validated_data["name"].replace(" ", "_")
        validated_data["username"] = self.generate_unique_username(base_username)
        
        user = User(
            last_login=timezone.now(),
            date_joined=timezone.now(),
            **validated_data
        )

        password = validated_data.get('password')
        if password:
            user.set_password(password)
        user.save()

        return user