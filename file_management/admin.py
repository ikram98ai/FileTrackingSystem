from django.contrib import admin
from .models import File, Department, Profile, Action

@admin.register(File)
class FileModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_type', 'from_department', 'to_department', 'created_at']
    search_fields = ['file_type', 'subject']
    ordering = ['created_at']

@admin.register(Department)
class DepartmentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['name']


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'department']
    ordering = ['user']



@admin.register(Action)
class ActionModelAdmin(admin.ModelAdmin):
    list_display = ['file', 'branch', 'action_taken','action_taken_at']
    ordering = ['action_taken_at']
