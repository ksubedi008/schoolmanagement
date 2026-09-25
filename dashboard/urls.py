from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/students/', views.admin_students, name='admin_students'),
    path('admin/parents/', views.admin_parents, name='admin_parents'),
    path('admin/staff/', views.admin_staff, name='admin_staff'),
    path('admin/academic/', views.admin_academic, name='admin_academic'),
    path('admin/system/', views.admin_system, name='admin_system'),
    path('student/', views.student_dashboard, name='student_dashboard'),
]
