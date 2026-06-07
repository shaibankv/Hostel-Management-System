from django.urls import path
from . import views

urlpatterns = [
    path('employee_list/',views.employee_list,name='employee_list'),
    path('add_employee/',views.add_employee,name='add_employee'),
    path('edit_employee/<int:id>/',views.edit_employee,name='edit_employee'),
    path('delete_employee/<int:id>/',views.delete_employee,name='delete_employee')
]