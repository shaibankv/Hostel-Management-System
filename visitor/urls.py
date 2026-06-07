from django.urls import path
from . import views

urlpatterns = [
    path('list_visitors/',views.list_visitors,name='list_visitors'),
    path('add_visitor/',views.add_visitor,name='add_visitor')
]