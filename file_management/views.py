from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


from .models import File, Action, Profile, Department
from .forms import FileUploadForm, SignUpForm

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            department = form.cleaned_data.get('department')
            Profile.objects.create(user=user, department=department)
            
            login(request, user)  # Log the user in after sign-up
            return redirect('branch_dashboard')
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
@user_passes_test(is_admin)
def upload_file(request):
    departments = Department.objects.all()

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('admin_dashboard')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form,'departments':departments})

# @login_required
# def branch_dashboard(request):
#     files = File.objects.filter(to_department__name=request.user.profile.department.name)
#     return render(request, 'branch_dashboard.html', {'files': files})


@login_required
def branch_dashboard(request):
    # Fetch files assigned to the current user's department
    user_department = request.user.profile.department
    files = File.objects.filter(to_department=user_department)
    departments = Department.objects.all()

    if request.method == "POST":
        action = request.POST.get('action')
        file_id = request.POST.get('file_id')
        file = get_object_or_404(File, id=file_id)
        # "Take Action" button logic
        if action == 'processed':
            file.status = 'Processed'
            file.save()
            messages.success(request, f'File {file.reference_number} has been processed.')
            return redirect('branch_dashboard')

          # Handle action from the modal
        if action == 'add_action':
            action_taken = request.POST.get('action_taken')
            print('action::',action_taken, file_id)

            if action_taken:
                # Save the action to the Action model
                Action.objects.create(
                    file=file,
                    branch=user_department,
                    action_taken=action_taken
                )
                messages.success(request, f'Action has been recorded for file {file.reference_number}.')
            else:
                messages.error(request, 'Please provide the action taken.')
            return redirect('branch_dashboard')
        
        # "Forward" button logic
        elif action == 'forwarded':
            new_department = request.POST.get('new_department')
            new_department = Department.objects.get(name = new_department)
            if new_department:
                file.from_department = user_department
                file.to_department = new_department
                file.status = 'Forwarded'
                file.save()
                messages.success(request, f'File {file.reference_number} has been forwarded to {new_department}.')
            else:
                messages.error(request, 'Please specify the department to forward to.')

            return redirect('branch_dashboard')

    context = {
        'files': files,
        'departments': departments
    }
    return render(request, 'branch_dashboard.html', context)



# Helper function to check if the user is a branch
def is_branch(user):
    return hasattr(user, 'department') and user.department is not None

# Admin View to show all actions on a file
@login_required
@user_passes_test(lambda u: u.is_superuser)  # Ensure only admin can access this view
def view_file_actions_admin(request, file_id):
    file = get_object_or_404(File, id=file_id)

    # Get all actions for the file
    actions = Action.objects.filter(file=file)

    return render(request, 'view_file_actions.html', {
        'file': file,
        'actions': actions
    })

# Branch View to show only branch-specific actions
@login_required
# @user_passes_test(is_branch)  # Ensure only branch users can access this view
def view_file_actions_branch(request, file_id):
    file = get_object_or_404(File, id=file_id)
    department = request.user.profile.department  # Get the department of the current user (branch)

    # Get actions related to this department
    actions = Action.objects.filter(file=file, branch=department)

    return render(request, 'view_file_actions.html', {
        'file': file,
        'actions': actions
    })