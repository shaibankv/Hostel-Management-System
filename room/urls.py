from django.urls import path
from . import views

urlpatterns = [
    path('room_list/',views.room_list,name = 'room_list'),
    path('add_room/',views.add_room,name='add_room'),
    path('edit_room/<int:id>/',views.edit_room,name='edit_room'),
    path('delete_room/<int:id>/',views.delete_room,name='delete_room'),
    path('room_students/<int:id>/',views.room_students,name='room_students'),
]