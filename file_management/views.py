from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


from .models import File, Action, Profile
from .forms import FileUploadForm, SignUpForm

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create a profile for branch users
            if not user.is_staff:
                department = form.cleaned_data.get('department')
                Profile.objects.create(user=user, department=department)
            
            login(request, user)  # Log the user in after sign-up
            return redirect('admin_dashboard' if user.is_staff else 'branch_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
# Check if user is admin
def is_admin(user):
    return user.is_staff

def home(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard' if request.user.is_staff else 'branch_dashboard')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard' if user.is_staff else 'branch_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'registration/login.html')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    files = File.objects.all()
    return render(request, 'admin_dashboard.html', {'files': files})

@login_required
def branch_dashboard(request):
    files = File.objects.filter(to_department__name=request.user.profile.department.name, status='Pending')
    return render(request, 'branch_dashboard.html', {'files': files})

@login_required
@user_passes_test(is_admin)
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('admin_dashboard')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})
