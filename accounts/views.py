from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import role_required
from student.models import Student
from complaints.models import Complaints
from room.models import Room
from django.db.models import Sum
from .models import UserList
from employee.models import Employee

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user:
            login(request,user) #Django's built in function which created user id 
            return redirect('dashboard')
        
        return render(request, 'login.html', {
            "error": "Invalid Username or Password"
        })
    return render(request,'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard_view(request):
    user = request.user

    if user.role == "Admin":
        students = Student.objects.all()
        student_count = Student.objects.count()
        total_capacity = Room.objects.aggregate(Sum('capacity'))['capacity__sum'] or 0
        available_rooms = total_capacity - student_count
        
        # Calculate overall fee stats
        total_hostel_fee = Student.objects.aggregate(total=Sum('hostel_fee'))['total'] or 0
        total_fees_collected = sum([s.fee_set.filter(status='Paid').aggregate(t=Sum('amount'))['t'] or 0 for s in students])
        total_pending_balance = total_hostel_fee - total_fees_collected

        return render(request, "admin_dashboard.html", {
            "students": students,
            "student_count": student_count,
            "available_rooms": available_rooms,
            "pending_complaints": Complaints.objects.filter(status="Pending").count(),
            "total_fees_collected": total_fees_collected,
            "total_pending_balance": total_pending_balance,
        })

    elif user.role == "Warden":
        complaints = Complaints.objects.all()
        pending_count = Complaints.objects.filter(status="Pending").count()
        in_progress_count = Complaints.objects.filter(status="In Progress").count()
        student_count = Student.objects.count()
        return render(request, "warden_dashboard.html", {
            "complaints": complaints,
            "pending_count": pending_count,
            "in_progress_count": in_progress_count,
            "student_count": student_count
        })

    elif user.role == "Staff":
        complaints = Complaints.objects.exclude(status="Solved").order_by("-date")
        pending_count = Complaints.objects.filter(status="Pending").count()
        in_progress_count = Complaints.objects.filter(status="In Progress").count()
        return render(request, "staff_dashboard.html", {
            "complaints": complaints,
            "pending_count": pending_count,
            "in_progress_count": in_progress_count,
        })

    elif user.role == "Student":
        student = getattr(user, 'student', None)
        fee_status_theme = "danger"
        fee_status_text = "Not Cleared"
        
        if student:
            paid_fee = student.fee_set.filter(status='Paid').aggregate(total=Sum('amount'))['total'] or 0
            total_fee = student.hostel_fee
            
            if paid_fee >= total_fee:
                fee_status_theme = "success"
                fee_status_text = "Cleared"
            elif paid_fee > 0:
                fee_status_theme = "warning"
                fee_status_text = "Partially Cleared"

        return render(request, "student_dashboard.html", {
            "fee_status_theme": fee_status_theme,
            "fee_status_text": fee_status_text
        })

    return redirect("login")

@role_required("Admin")
def add_user(request):
        
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if UserList.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'add_user.html', {'error': 'Username already exists. Please choose a different one.'})
            
        user = UserList.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        user.plain_password = password
        user.save()
        messages.success(request, f"User '{username}' created successfully.")
        return redirect('manage_users')
        
    return render(request, 'add_user.html')

@login_required
def profile_view(request):
    user = request.user
    
    employee = None
    if user.role in ['Warden', 'Staff']:
        employee = Employee.objects.filter(user=user).first()
        
    return render(request, 'profile.html', {
        'user': user,
        'employee': employee
    })


@role_required("Admin")
def edit_admin_profile(request):
        
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Check if username exists and belongs to someone else
        if username and username != request.user.username and UserList.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
            return render(request, 'edit_admin_profile.html', {
                'error': 'Username already exists. Please choose another.'
            })
            
        if username:
            request.user.username = username
        if email is not None:
            request.user.email = email
        if first_name is not None:
            request.user.first_name = first_name
        if last_name is not None:
            request.user.last_name = last_name
            
        request.user.save()
        
        # Redirect to dashboard or show success message
        messages.success(request, "Admin profile updated successfully.")
        return redirect('dashboard')
        
    return render(request, 'edit_admin_profile.html')


@role_required("Admin")
def manage_users(request):
    
    users = UserList.objects.all()
    admins = UserList.objects.filter(role="Admin")
    wardens = UserList.objects.filter(role="Warden")
    staff = UserList.objects.filter(role="Staff")
    students = UserList.objects.filter(role="Student")
    
    return render(request, 'manage_users.html', {
        'users': users,
        'admins': admins,
        'wardens': wardens,
        'staff': staff,
        'students': students,
    })


@role_required("Admin")
def edit_user(request, user_id):
        
    user = get_object_or_404(UserList, id=user_id)
    if request.method == "POST":
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_role = request.POST.get('role')
        new_password = request.POST.get('password')
        
        if new_username and new_username != user.username:
            if UserList.objects.filter(username=new_username).exists():
                messages.error(request, f"Username '{new_username}' is already taken.")
                return redirect('manage_users')
            user.username = new_username
            
        if new_email:
            user.email = new_email
            
        if new_role:
            user.role = new_role
            
        if new_password:
            user.set_password(new_password)
            user.plain_password = new_password
            
        user.save()
        messages.success(request, f"User '{user.username}' details updated successfully.")
        
    return redirect('manage_users')


@role_required("Admin")
def delete_user(request, user_id):
        
    if request.user.id == user_id:
        messages.error(request, "You cannot delete your own admin account.")
        return redirect('manage_users')
        
    user = get_object_or_404(UserList, id=user_id)
    username = user.username
    user.delete()
    messages.success(request, f"User '{username}' deleted successfully.")
    return redirect('manage_users')

def custom_404_view(request, exception=None):
    return redirect('login')
