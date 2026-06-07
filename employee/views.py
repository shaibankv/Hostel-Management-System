from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Employee
from accounts.models import UserList

# Create your views here.

#view to list the employees
@role_required("Admin")
def employee_list(request):
    
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees':employees})

#view to add employees
@role_required("Admin")
def add_employee(request):
    
    if request.method == "POST":
        user_id = request.POST.get('user')
        user = get_object_or_404(UserList, id=user_id) if user_id else None

        name = request.POST.get('name')
        role = request.POST.get('role')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        salary = request.POST.get('salary')
        shift = request.POST.get('shift')
        block = request.POST.get('block') if role == 'Warden' else None

        Employee.objects.create(
            user = user,
            name = name,
            role = role,
            phone = phone,
            email = email,
            salary = salary,
            shift = shift,
            block = block,
        )
        messages.success(request, f"Employee '{name}' added successfully.")
        return redirect('employee_list')
    users = UserList.objects.filter(role__in=['Warden', 'Staff'])
    return render(request,'add_employee.html', {'users': users})

#view to edit employee
@role_required("Admin")
def edit_employee(request,id):
    
    employee = Employee.objects.get(id=id)
    
    if request.method == "POST":
        employee.name = request.POST.get('name')
        employee.role = request.POST.get('role')
        employee.phone = request.POST.get('phone')
        employee.email = request.POST.get('email')
        employee.salary = request.POST.get('salary')
        employee.shift = request.POST.get('shift')
        employee.block = request.POST.get('block') if employee.role == 'Warden' else None

        employee.save()

        messages.success(request, f"Employee '{employee.name}' details updated successfully.")
        return redirect('employee_list')
    return render(request,'edit_employee.html',{'employee':employee})

#view to delete an employee
@role_required("Admin")
def delete_employee(request,id):
    
    employee = Employee.objects.get(id=id)

    if request.method == "POST":
        employee.delete()
        messages.success(request, f"Employee '{employee.name}' deleted successfully.")
        return redirect('employee_list')
    return render(request,'delete_employee.html',{'employee':employee})
    


    

    






