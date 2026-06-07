from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Sum
from django.contrib import messages
from accounts.decorators import role_required
from .models import Student, Fee

# Create your views here.

#view to add fee details
@role_required("Admin")
def add_fee(request,id):
    
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        academic_year = request.POST.get('academic_year')
        status = request.POST.get('status')
        payment_method = request.POST.get('payment_method') 
        transaction_id = request.POST.get('transaction_id')

        Fee.objects.create(
            student=student,
            amount = amount,
            payment_date = payment_date,
            academic_year = academic_year,
            status = status,
            payment_method = payment_method,
            transaction_id = transaction_id
        )     

        if status == 'Paid':
            messages.success(request, f"Fee payment of Rs. {amount} recorded successfully. A confirmation email with the receipt has been sent to the student.")
        else:
            messages.success(request, f"Fee payment record of Rs. {amount} added with status '{status}'.")
        return redirect('student_fee', id=student.id)
    return render(request,'add_fee.html',{'student':student})


#view to list fee details
@role_required("Admin")
def fee_list(request):
    
    students = Student.objects.all()
    total_hostel_fee = 0
    total_paid_fee = 0

    for student in students:
        paid = student.fee_set.filter(status='Paid').aggregate(total=Sum('amount'))['total'] or 0
        student.paid_fee = paid
        student.balance_fee = student.hostel_fee - student.paid_fee
        student.fee_status = "Completed" if student.balance_fee <= 0 else "Pending"
        
        total_hostel_fee += student.hostel_fee
        total_paid_fee += paid

    total_balance_fee = total_hostel_fee - total_paid_fee

    return render(request,'fee_list.html',{
        'students': students,
        'total_hostel_fee': total_hostel_fee,
        'total_paid_fee': total_paid_fee,
        'total_balance_fee': total_balance_fee
    })


#view for the student to view the fee details
@login_required(login_url = "login")
def student_fee(request,id):
    student = get_object_or_404(Student, id=id)
    if request.user.role == 'Student' and student.user != request.user:
        logout(request)
        messages.error(request, "Unauthorized access. You have been logged out.")
        return redirect('login')

    fee = Fee.objects.filter(student=student).order_by('-payment_date')
    
    paid_fee = fee.filter(status='Paid').aggregate(total=Sum('amount'))['total'] or 0
    balance_fee = student.hostel_fee - paid_fee

    return render(request, 'student_fee.html',{
        'student': student,
        'fee': fee,
        'paid_fee': paid_fee,
        'balance_fee': balance_fee
    })




