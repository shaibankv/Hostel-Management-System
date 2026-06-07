from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from accounts.decorators import role_required
from .models import Student
from fee.models import Fee
from room.models import Room
from accounts.models import UserList

# Create your views here.

#view to list the students from the database
@login_required(login_url = "login")
def student_list(request):
     if request.user.role == "Admin":
        students = Student.objects.all()
        return render(request, 'student_list.html', {'students': students})
     elif request.user.role == "Warden":
        students = Student.objects.all()
        return render(request, 'student_list.html', {'students': students})
     elif request.user.role == "Staff":
        students = Student.objects.all()
        return render(request, 'student_list.html', {'students': students})
     elif request.user.role == "Student":
        student = get_object_or_404(Student, user=request.user)
        return render(request, "student_dashboard.html", {"student": student})

        
#view to add student to the database
@role_required("Admin")
def add_student(request):
    if request.method == "POST":
        user_id = request.POST.get('user')
        user = get_object_or_404(UserList, id=user_id)
        reg_number = request.POST.get('reg_number')

        if Student.objects.filter(user=user).exists():
            messages.error(request, "A student profile for this user already exists.")
            return render(request, "add_student.html", {"error": "A student profile for this user already exists.",
                "users":UserList.objects.filter(role="Student"),
                "rooms":Room.objects.all(),
                "fees":Fee.objects.all(),
            })

        if Student.objects.filter(reg_number=reg_number).exists():
            messages.error(request, f"A student with registration number {reg_number} already exists.")
            return render(request, "add_student.html", {"error": f"A student with registration number {reg_number} already exists.",
                "users":UserList.objects.filter(role="Student"),
                "rooms":Room.objects.all(),
                "fees":Fee.objects.all(),
            })

        name = request.POST.get('name')
        dob = request.POST.get('dob')
        course = request.POST.get('course')
        year = request.POST.get('year')

        hostel_fee = request.POST.get('hostel_fee')
        if not hostel_fee:
            hostel_fee = 0

        phone = request.POST.get('phone')
        email = request.POST.get('email')
        home_address = request.POST.get('home_address')

        guardian_name = request.POST.get('guardian_name')
        guardian_phone = request.POST.get('guardian_phone')
        guardian_email = request.POST.get('guardian_email')

        room_id = request.POST.get('room')
        room = get_object_or_404(Room, id=room_id)

        student_count = Student.objects.filter(room=room).count()
        if student_count >= room.capacity:
            messages.error(request, f"Cannot add student. Room {room.room_no} is full.")
            return render(request, "add_student.html", {"error": f"Cannot add student. Room {room.room_no} in Block {room.block} is already at full capacity ({room.capacity}).",
                "users":UserList.objects.filter(role="Student"),
                "rooms":Room.objects.all(),
                "fees":Fee.objects.all(),
            })

        photo = request.FILES.get('photo')

        id_proof = request.FILES.get('id_proof')

        student = Student.objects.create(
            user = user,
            name = name,
            reg_number = reg_number,
            dob = dob,
            course = course,
            year = year,
            hostel_fee = hostel_fee,
            phone = phone,
            email = email,
            home_address = home_address,
            guardian_name = guardian_name,
            guardian_phone = guardian_phone,
            guardian_email = guardian_email,
            room = room,
            photo = photo,
            id_proof = id_proof,
        )

        # Look up Warden details for the room's block
        from employee.models import Employee
        from django.core.mail import send_mail
        from django.conf import settings

        warden = None
        if student.room and student.room.block:
            warden = Employee.objects.filter(role='Warden', block=student.room.block).first()
            if not warden:
                # Fallback to any Warden in the system
                warden = Employee.objects.filter(role='Warden').first()

        if warden:
            warden_name = warden.name
            warden_phone = warden.phone
            warden_email = warden.email
        else:
            warden_name = "Not Assigned"
            warden_phone = "N/A"
            warden_email = "N/A"

        # Prepare and send welcome email
        subject = "Welcome to SEA Hostel Management System!"
        message_body = (
            f"Dear {student.name},\n\n"
            f"Welcome to the SEA Hostel! You have been successfully registered in our system.\n\n"
            f"Here are your room details:\n"
            f"- Room Number: {student.room.room_no if student.room else 'N/A'}\n"
            f"- Block: {student.room.block if student.room else 'N/A'}\n\n"
            f"Your Block Warden's contact details:\n"
            f"- Name: {warden_name}\n"
            f"- Phone: {warden_phone}\n"
            f"- Email: {warden_email}\n\n"
            f"If you have any questions or require assistance, please feel free to reach out to your Block Warden.\n\n"
            f"Best regards,\n"
            f"SEA Hostel Administration"
        )

        email_sent = False
        try:
            send_mail(
                subject=subject,
                message=message_body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@seahsm.com'),
                recipient_list=[email],
                fail_silently=False,
            )
            email_sent = True
        except Exception as e:
            # We catch exceptions so that a mail server failure doesn't block student registration.
            messages.warning(request, f"Student '{name}' added successfully, but welcome email could not be sent. Error: {e}")

        if email_sent:
            messages.success(request, f"Student '{name}' added successfully. Welcome email sent.")
        
        return redirect('student_list')
    return render(request, "add_student.html", {
        "users":UserList.objects.filter(role="Student"),
        "rooms":Room.objects.all(),
        "fees":Fee.objects.all(),
    })


#view to update student details 
@role_required("Admin")
def edit_student(request,id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.name = request.POST.get('name')
        student.reg_number = request.POST.get('reg_number')
        student.dob = request.POST.get('dob')
        student.course = request.POST.get('course')
        student.year = request.POST.get('year')

        hostel_fee = request.POST.get('hostel_fee')
        if hostel_fee:
            student.hostel_fee = hostel_fee
        else:
            student.hostel_fee = 0

        student.phone = request.POST.get('phone')
        student.email = request.POST.get('email')
        student.home_address = request.POST.get('home_address')

        student.guardian_name = request.POST.get('guardian_name')
        student.guardian_phone = request.POST.get('guardian_phone')
        student.guardian_email = request.POST.get('guardian_email')

        room_id = request.POST.get('room')
        student.room = get_object_or_404(Room, id=room_id)

        photo = request.FILES.get('photo')
        if photo:
            student.photo = photo

        id_proof = request.FILES.get('id_proof')
        if id_proof:
            student.id_proof = id_proof
            
        student.save()
        messages.success(request, f"Student '{student.name}' details updated successfully.")
        return redirect('student_list')
    return render(request,'edit_student.html',{'student':student, 'rooms':Room.objects.all()})

#view for the student to update the details

@role_required('Student')
def update_profile(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.dob = request.POST.get('dob')
        student.phone = request.POST.get('phone')
        student.email = request.POST.get('email')
        student.home_address = request.POST.get('home_address')
        
        # Photo handling
        photo = request.FILES.get('photo')
        if photo:
            student.photo = photo
            
        student.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('student_list')
    return render(request, 'update_profile.html', {'student': student})

#view to delete a field 
@role_required("Admin")
def delete_student(request,id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, f"Student '{student.name}' deleted successfully.")
        return redirect('student_list')
    return render(request,'delete_student.html',{'student':student})

#view to see student details
@login_required(login_url="login")
def view_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.user.role == 'Student' and student.user != request.user:
        logout(request)
        messages.error(request, "Unauthorized access. You have been logged out.")
        return redirect('login')
    return render(request, 'view_student.html', {'student': student})

@role_required('Student')
def my_room(request):
    
    student = get_object_or_404(Student, user=request.user)
    room = student.room
    roommates = []
    
    if room:
        roommates = room.student_set.exclude(id=student.id)
        
    return render(request, 'my_room.html', {'student': student, 'room': room, 'roommates': roommates})