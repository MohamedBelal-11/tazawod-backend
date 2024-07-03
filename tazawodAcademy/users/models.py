from django.db import models

# Create your models here.

from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=55, unique=True)

    user_type = models.CharField(max_length=10, choices=[
        ("student", "Student"),
        ("teacher", "Teacher")
    ])

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    # is_verified = models.BooleanField(default=False)
    # otp = models.IntegerField(null=True, blank=True)  # Field to store OTP

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_set',  # Add related_name to avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set',  # Add related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["phone_number", "name"]

    def __str__(self):
        return self.username

class StudentData(models.Model):
    subscribed = models.BooleanField(default=False)
    student = models.OneToOneField(User, on_delete=models.CASCADE)

class TeacherData(models.Model):
    is_accepted = models.BooleanField(default=False)
    teacher = models.OneToOneField(User, on_delete=models.CASCADE)

class QuraanDays(models.Model):
    DAY_CHOICES = [
        ("sunday", "sunday"),
        ("monday", "monday"),
        ("tuesday", "tuesday"),
        ("wednesday", "wednesday"),
        ("thurusday", "thurusday"),
        ("friday", "friday"),
        ("saturday", "saturday"),
    ]
    day = models.CharField(max_length=9, choices=DAY_CHOICES,)
    starts = models.TimeField()
    delay = models.DurationField()
    student = models.ForeignKey(StudentData, on_delete=models.CASCADE)
