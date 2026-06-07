from django.urls import path
from . import views

urlpatterns = [
    path('student_list/',views.student_list,name='student_list'),
    path('add_student/',views.add_student,name='add_student'),
    path('edit_student/<int:id>/',views.edit_student,name='edit_student'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('delete_student/<int:id>/',views.delete_student,name='delete_student'),
    path('view_student/<int:id>/',views.view_student,name='view_student'),
    path('my_room/',views.my_room,name='my_room'),
]