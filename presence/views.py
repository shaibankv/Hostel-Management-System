from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.decorators import role_required
from .models import Presence
from student.models import Student
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.

def send_guardian_notification(student, record, type):
    """Helper to send entry/exit emails to guardians"""
    if not student.guardian_email:
        return

    if type == "exit":
        subject = f"Hostel Exit Notification: {student.name}"
        message = f"Dear Guardian,\n\nThis is to inform you that {student.name} has signed OUT of the hostel.\n\n" \
                  f"Exit Date: {record.date_out}\n" \
                  f"Exit Time: {record.time_out}\n" \
                  f"Reason: {record.reason}\n\n" \
                  f"Regards,\nSEA Hostel Administration"
    else:
        subject = f"Hostel Entry Notification: {student.name}"
        message = f"Dear Guardian,\n\nThis is to inform you that {student.name} has signed IN to the hostel.\n\n" \
                  f"Entry Date: {record.date_in}\n" \
                  f"Entry Time: {record.time_in}\n\n" \
                  f"Regards,\nSEA Hostel Administration"

    try:
        send_mail(subject, message, None, [student.guardian_email])
    except Exception as e:
        print(f"Error sending email: {e}")

#view to mark out
@role_required(["Admin", "Warden"])
def mark_out(request,id):
    student = Student.objects.get(id=id)

    if request.method == 'POST':
        record = Presence.objects.create(
            student=student,
            date_out=timezone.now().date(),
            time_out=timezone.now().time(),
            status="Outside",
            reason=request.POST.get("reason")
        )

        send_guardian_notification(student, record, "exit")
        messages.success(request, f"Successfully marked OUT for {student.name}. Exit notification email sent to guardian.")
        return redirect("presence_list")

    return render(request, "mark_out.html", {"student": student})


#view to mark in
@role_required(["Admin", "Warden"])
def mark_in(request,id):
    
    record = Presence.objects.get(id=id)

    record.date_in = timezone.now().date()
    record.time_in = timezone.now().time()
    record.status = "Inside"

    record.save()
    send_guardian_notification(record.student, record, "entry")
    messages.success(request, f"Successfully marked IN for {record.student.name}. Entry notification email sent to guardian.")
    return redirect("presence_list")

#view to display the list
@role_required(["Admin", "Warden"])
def presence_list(request):
    
    records = Presence.objects.all().order_by("-date_out")

    return render(request, "presence_list.html", {"records": records})


# view to add a presence record manually
@role_required(["Admin", "Warden"])
def add_presence(request):

    students = Student.objects.all().order_by("name")

    if request.method == "POST":
        student_id = request.POST.get("student")
        date_out   = request.POST.get("date_out")
        time_out   = request.POST.get("time_out")
        reason     = request.POST.get("reason", "")

        if student_id and date_out and time_out:
            student = Student.objects.get(id=student_id)
            record = Presence.objects.create(
                student=student,
                date_out=date_out,
                time_out=time_out,
                status="Outside",
                reason=reason,
            )
            send_guardian_notification(student, record, "exit")
            messages.success(request, "Attendance record added successfully.")
            return redirect("presence_list")
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, "add_presence.html", {"students": students})

