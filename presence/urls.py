from django.urls import path
from . import views

urlpatterns = [
    path('mark_out/<int:id>/',views.mark_out,name='mark_out'),
    path('mark_in/<int:id>/',views.mark_in,name='mark_in'),
    path('presence_list/',views.presence_list,name='presence_list'),
    path('add_presence/',views.add_presence,name='add_presence'),
]