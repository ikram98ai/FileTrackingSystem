from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Department, File

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_staff = forms.BooleanField(
        required=False,
        label='Register as Admin',
        help_text='Check this if you are registering as an admin'
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        help_text='Select your branch if you are not an admin'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff', 'department']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = self.cleaned_data['is_staff']
        if commit:
            user.save()
        return user

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'file_data', 'file_type', 'priority', 'purpose', 'from_department', 'to_department', 'file_source', 'subject', 'description']
