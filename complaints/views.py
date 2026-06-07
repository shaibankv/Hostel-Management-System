from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Complaints

# Create your views here.

#view to list the complaints
@login_required(login_url='login')
def list_complaints(request):
    complaints = Complaints.objects.all()

    return render(request,'list_complaints.html',{'complaints':complaints})

#view to add a coimplaint
@role_required("Student")
def add_complaint(request):
     
     if request.method == 'POST':
         name = request.POST.get('name')
         block = request.POST.get('block')
         room_no = request.POST.get('room_no')
         complaint = request.POST.get('complaint')
         description = request.POST.get('description')

         Complaints.objects.create(
             name = name,
             block = block,
             room_no = room_no,
             complaint = complaint,
             description = description,
         )
         messages.success(request, "Your complaint has been registered successfully.")
         return redirect('dashboard')
     return render(request,'add_complaint.html')

#view to solve the complaint
@role_required(["Admin", "Warden", "Staff"])
def solve_complaint(request, id):
    if request.method == 'POST':
        complaint = Complaints.objects.get(id=id)
        complaint.status = "Solved"
        complaint.save()
        messages.success(request, "Complaint marked as solved.")
        return redirect('list_complaints')

@role_required(["Admin", "Warden", "Staff"])
def in_progress_complaint(request, id):
    if request.method == 'POST':
        complaint = Complaints.objects.get(id=id)
        complaint.status = "In Progress"
        complaint.save()
        messages.success(request, "Complaint status updated to In Progress.")
        return redirect('list_complaints')


def dashboard(request):
    complaints = Complaints.objects.all()

    pending_count = Complaints.objects.filter(status="Pending").count()
    in_progress_count = Complaints.objects.filter(status="In Progress").count()

    context = {
        "complaints": complaints,
        "pending_count": pending_count,
        "in_progress_count": in_progress_count,
    }

    return render(request, "warden_dashboard.html", context)