from django.urls import path
from . import views, export_views

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
    path('admin/students/details/<int:pk>/', views.student_details_partial, name='student_details_partial'),
    path('admin/students/table/', views.student_table_partial, name='student_table_partial'),
    path('admin/students/delete/<int:pk>/', views.soft_delete_student, name='soft_delete_student'),
    
    path('admin/teachers/table/', views.teacher_table_partial, name='teacher_table_partial'),
    path('admin/teachers/details/<int:pk>/', views.teacher_details_partial, name='teacher_details_partial'),
    path('admin/teachers/delete/<int:pk>/', views.soft_delete_teacher, name='soft_delete_teacher'),
    
    path('admin/parents/table/', views.parent_table_partial, name='parent_table_partial'),
    path('admin/parents/details/<int:pk>/', views.parent_details_partial, name='parent_details_partial'),
    path('admin/parents/delete/<int:pk>/', views.soft_delete_parent, name='soft_delete_parent'),
    
    path('admin/system/users/table/', views.user_table_partial, name='user_table_partial'),
    path('admin/system/users/delete/<int:pk>/', views.soft_delete_user, name='soft_delete_user'),
    
    path('admin/academic/delete/<str:model_type>/<int:pk>/', views.soft_delete_academic, name='soft_delete_academic'),
    path('admin/academic/class/details/<int:pk>/', views.class_details_partial, name='class_details_partial'),
    path('admin/academic/class/students/<int:pk>/', views.class_students_partial, name='class_students_partial'),
    path('admin/academic/class/parents/<int:pk>/', views.class_parents_partial, name='class_parents_partial'),
    path('admin/academic/class/assign-subjects/<int:pk>/', views.assign_class_subjects, name='assign_class_subjects'),
    path('admin/academic/subject/details/<int:pk>/', views.subject_details_partial, name='subject_details_partial'),
    path('admin/academic/subject/assign-classes/<int:pk>/', views.assign_subject_classes, name='assign_subject_classes'),
    
    path('admin/students/bulk-assign-electives/<int:class_id>/<int:section_id>/', views.bulk_assign_electives_view, name='bulk_assign_electives_view'),
    path('admin/students/api/bulk-assign-electives/', views.bulk_assign_electives_api, name='bulk_assign_electives_api'),
    path('api/sections/', views.api_get_sections, name='api_get_sections'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('parent/', views.parent_dashboard, name='parent_dashboard'),

    path('admin/students/export/', export_views.export_students_csv, name='export_students_csv'),
    path('admin/parents/export/', export_views.export_parents_csv, name='export_parents_csv'),
    path('admin/users/reset-password/<int:user_id>/', export_views.reset_user_password, name='reset_user_password'),
]
