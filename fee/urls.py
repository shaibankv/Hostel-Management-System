from django.urls import path
from . import views

urlpatterns = [
    path('add_fee/<int:id>/',views.add_fee,name='add_fee'),
    path('fee_list/',views.fee_list,name='fee_list'),
    path('student_fee/<int:id>/',views.student_fee,name='student_fee'),
]