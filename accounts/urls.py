from django.urls import path
from . import views

urlpatterns = [
path('',views.login_view,name='login'),
path('dashboard/',views.dashboard_view,name='dashboard'),
path('logout/',views.logout_view,name='logout'),
path('add_user/',views.add_user,name='add_user'),
path('profile/',views.profile_view,name='profile'),
path('edit_admin_profile/',views.edit_admin_profile,name='edit_admin_profile'),
path('manage_users/',views.manage_users,name='manage_users'),
path('manage_users/edit/<int:user_id>/',views.edit_user,name='edit_user'),
path('manage_users/delete/<int:user_id>/',views.delete_user,name='delete_user'),
]