import os

# Update URLs
urls_path = 'dashboard/urls.py'
with open(urls_path, 'r', encoding='utf-8') as f:
    urls_content = f.read()

new_urls = """    path('admin/students/bulk-assign-electives/<int:class_id>/<int:section_id>/', views.bulk_assign_electives_view, name='bulk_assign_electives_view'),
    path('admin/students/api/bulk-assign-electives/', views.bulk_assign_electives_api, name='bulk_assign_electives_api'),"""

if 'bulk-assign-electives' not in urls_content:
    urls_content = urls_content.replace("    path('api/sections/', views.api_get_sections, name='api_get_sections'),", new_urls + "\n    path('api/sections/', views.api_get_sections, name='api_get_sections'),")
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls_content)
    print("URLs updated")

# Update Views
views_path = 'dashboard/views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

new_views = """
@login_required
def bulk_assign_electives_view(request, class_id, section_id):
    if not (request.user.is_superuser or request.user.has_scope_permission("dashboard.admin.view")):
        raise PermissionDenied()
    
    from students.models import AcademicClass, Section, Student, ElectiveGroup
    
    academic_class = get_object_or_404(AcademicClass, pk=class_id)
    section = get_object_or_404(Section, pk=section_id, academic_class=academic_class)
    
    students = Student.objects.filter(current_class=academic_class, current_section=section, is_deleted=False).order_by('roll_number', 'first_name')
    elective_groups = ElectiveGroup.objects.filter(academic_class=academic_class).prefetch_related('subjects')
    
    return render(request, 'dashboard/modules/bulk_assign_electives.html', {
        'academic_class': academic_class,
        'section': section,
        'students': students,
        'elective_groups': elective_groups,
    })

@login_required
def bulk_assign_electives_api(request):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission("dashboard.admin.view")):
            return JsonResponse({'success': False, 'error': 'Permission denied'})
        
        try:
            import json
            from django.db import transaction
            from students.models import Student, Subject
            
            data = json.loads(request.body)
            assignments = data.get('assignments', []) # [{'student_id': 1, 'subject_ids': [2, 3]}]
            
            with transaction.atomic():
                for assignment in assignments:
                    student_id = assignment.get('student_id')
                    subject_ids = assignment.get('subject_ids', [])
                    
                    student = Student.objects.get(pk=student_id)
                    student.elective_subjects.set(subject_ids)
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
"""

if 'def bulk_assign_electives_view' not in views_content:
    with open(views_path, 'a', encoding='utf-8') as f:
        f.write(new_views)
    print("Views updated")
