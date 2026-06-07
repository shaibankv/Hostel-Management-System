from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Student, Visitor

# Create your views here.


#view to list the visitors
@role_required(["Admin", "Warden"])
def list_visitors(request):
    
    visitors = Visitor.objects.all()

    return render(request,'list_visitors.html',{'visitors':visitors})


#view to add a visitor
@role_required(["Admin", "Warden"])
def add_visitor(request):

    if request.method == 'POST':
        student_id = request.POST.get('student')
        student = get_object_or_404(Student, id=student_id)

        visitor_name = request.POST.get('visitor_name')
        visit_date = request.POST.get('visit_date')
        visit_time = request.POST.get('visit_time')
        visit_reason = request.POST.get('visit_reason')

        Visitor.objects.create(
            student = student,
            visitor_name = visitor_name,
            visit_date = visit_date,
            visit_time = visit_time,
            visit_reason = visit_reason,
        )
        messages.success(request, f"Visitor record for '{visitor_name}' added successfully.")
        return redirect('list_visitors')
    return render(request,'add_visitor.html',{'students': Student.objects.all()})

