from django.db import models
from django.contrib.auth.models import User
import uuid



class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class File(models.Model):
    PRIORITY_CHOICES = [('Normal', 'Normal'), ('Urgent', 'Urgent')]
    
    reference_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    file_name = models.CharField(max_length=100)
    file_data = models.FileField(upload_to='uploaded_files/')
    file_type = models.CharField(max_length=50)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    purpose = models.TextField()
    from_department = models.ForeignKey(Department, related_name='sent_files',  null=True, blank=True, on_delete=models.CASCADE)
    to_department = models.ForeignKey(Department, related_name='received_files', on_delete=models.CASCADE)
    file_source = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class Action(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    branch = models.ForeignKey(Department, on_delete=models.CASCADE)
    action_taken = models.CharField(max_length=100)
    action_taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Action on {self.file.reference_number}"
