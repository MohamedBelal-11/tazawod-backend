from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=55, unique=True)

    user_type = models.CharField(max_length=10, choices=[
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
        ("superadmin", "SuperAdmin"),
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

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.phone_number

class StudentData(models.Model):
    subscribed = models.BooleanField(default=False)
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        "TeacherData",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

class TeacherData(models.Model):
    WORK_TIME_CHOICES = [
        ("morning", "Morning"),
        ("afternoon", "Afternoon"),
        ("night", "Night"),
    ]

    prefered_time = models.CharField(max_length=10, choices=WORK_TIME_CHOICES)
    about = models.TextField(max_length=400, null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    teacher = models.OneToOneField(User, on_delete=models.CASCADE)

class AdminData(models.Model):
    is_accepted = models.BooleanField(default=False)
    about = models.TextField(max_length=400, null=True, blank=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)

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
