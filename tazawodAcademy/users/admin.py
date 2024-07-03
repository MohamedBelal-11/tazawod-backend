from django.contrib import admin
from .models import User, StudentData, QuraanDays, TeacherData

# Register your models here.

admin.site.register(User)
admin.site.register(StudentData)
admin.site.register(QuraanDays)
admin.site.register(TeacherData)
