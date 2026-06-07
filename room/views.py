from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Room
from django.db.models import Count

# Create your views here.

#view to list the room 
@role_required(["Admin", "Warden"])
def room_list(request):
   
    rooms = Room.objects.annotate(student_count=Count('student'))

    for room in rooms:
        room.vacancy = room.capacity-room.student_count

    return render(request,'room_list.html',{'rooms':rooms})

#view to add the room
@role_required(["Admin", "Warden"])
def add_room(request):
    if request.method == 'POST':
        block = request.POST.get('block')
        room_no = request.POST.get('room_no')
        capacity = request.POST.get('capacity')
        
        Room.objects.create(
            block = block,
            room_no = room_no,
            capacity = capacity,
        )
        messages.success(request, f"Room '{room_no}' in Block '{block}' created successfully.")
        return redirect('room_list')
    return render(request, "add_room.html")

#view to edit room details
@role_required(["Admin", "Warden"])
def edit_room(request,id):
    
    room = get_object_or_404(Room, id=id)
    if request.method == "POST":
        room.block = request.POST.get('block')
        room.room_no = request.POST.get('room_no')
        room.capacity = request.POST.get('capacity')
        room.save()
        
        messages.success(request, f"Room '{room.room_no}' details updated successfully.")
        return redirect('room_list')
    return render(request, 'edit_room.html', {'room':room})

#view to delete the room
@role_required(["Admin", "Warden"])
def delete_room(request,id):
    
    room = get_object_or_404(Room, id=id)
    
    if request.method == "POST":
        room.delete()
        messages.success(request, f"Room '{room.room_no}' deleted successfully.")
        return redirect('room_list')
    return render(request,'delete_room.html',{'room':room})

@role_required(["Admin", "Warden"])
def room_students(request, id):
    
    room = get_object_or_404(Room, id=id)
    students = room.student_set.all()
    
    return render(request, 'room_students.html', {'room': room, 'students': students})
