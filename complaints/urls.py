from django.urls import path
from . import views

urlpatterns = [
    path('list_complaints/',views.list_complaints,name='list_complaints'),
    path('add_complaint/',views.add_complaint,name='add_complaint'),
    path('solve_complaint/<int:id>/',views.solve_complaint,name='solve_complaint'),
    path('in_progress_complaint/<int:id>/',views.in_progress_complaint,name='in_progress_complaint'),
]