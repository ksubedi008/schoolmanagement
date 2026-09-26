import csv
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch

from accounts.models import User
from students.models import Student, Parent, Section
from dashboard.models import SchoolProfile

@login_required
def export_students_csv(request):
    if not (request.user.is_superuser or request.user.has_scope_permission("dashboard.admin.view")):
        raise PermissionDenied()
        
    include_credentials = request.GET.get('include_credentials') == 'true'
    
    # Get School Profile
    school = SchoolProfile.objects.first()
    school_name = school.name if school else "My School"
    school_address = school.address if school else ""
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="students_export.csv"'},
    )

    writer = csv.writer(response)
    
    # Write headers
    headers = [
        "School Name", "School Location", 
        "Class & Section", "Class Teacher", "Teacher Phone",
        "Student Name", "Roll Number", "Student ID", 
        "Parent Name", "Parent Phone", "Parent Location"
    ]
    if include_credentials:
        headers.append("Initial Temp Password")
        
    writer.writerow(headers)
    
    # Query Students efficiently
    students = Student.objects.filter(is_deleted=False).select_related(
        'current_class', 'current_section', 'current_section__class_teacher', 'user'
    ).prefetch_related(
        Prefetch('parents', queryset=Parent.objects.filter(is_deleted=False))
    )

    selected_ids = request.GET.get('selected_ids')
    if selected_ids:
        ids_list = [int(i.strip()) for i in selected_ids.split(',') if i.strip().isdigit()]
        if ids_list:
            students = students.filter(id__in=ids_list)
    
    for student in students:
        class_section = f"{student.current_class.name if student.current_class else ''} - {student.current_section.name if student.current_section else ''}"
        
        teacher = student.current_section.class_teacher if student.current_section else None
        teacher_name = f"{teacher.first_name} {teacher.last_name}" if teacher else ""
        teacher_phone = teacher.phone_number if teacher else ""
        
        student_name = f"{student.first_name} {student.last_name}"
        
        parent = student.parents.first() # Getting primary parent
        parent_name = f"{parent.first_name} {parent.last_name}" if parent else ""
        parent_phone = parent.phone_number if parent else ""
        parent_location = parent.address if parent else ""
        
        row = [
            school_name, school_address,
            class_section, teacher_name, teacher_phone,
            student_name, student.roll_number, student.admission_number,
            parent_name, parent_phone, parent_location
        ]
        
        if include_credentials:
            if student.user:
                if student.user.initial_temp_password:
                    row.append(student.user.initial_temp_password)
                else:
                    row.append("Already Set")
            else:
                row.append("No Account")
                
        writer.writerow(row)

    return response


@login_required
def export_parents_csv(request):
    if not (request.user.is_superuser or request.user.has_scope_permission("dashboard.admin.view")):
        raise PermissionDenied()
        
    include_credentials = request.GET.get('include_credentials') == 'true'
    
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="parents_export.csv"'},
    )

    writer = csv.writer(response)
    
    headers = [
        "Class & Section (Primary Child)", 
        "Parent Name", "Relationship", "Phone Number", "Location",
        "Associated Student Name(s)"
    ]
    if include_credentials:
        headers.append("Initial Temp Password")
        
    writer.writerow(headers)
    
    # Sort primarily by child's class/section. Using prefetch_related for children
    parents = Parent.objects.filter(is_deleted=False).select_related('user').prefetch_related(
        Prefetch('children', queryset=Student.objects.select_related('current_class', 'current_section'))
    ).order_by('children__current_class__name', 'children__current_section__name').distinct()
    
    selected_ids = request.GET.get('selected_ids')
    if selected_ids:
        ids_list = [int(i.strip()) for i in selected_ids.split(',') if i.strip().isdigit()]
        if ids_list:
            parents = parents.filter(id__in=ids_list)
    
    for parent in parents:
        children = list(parent.children.all())
        primary_child = children[0] if children else None
        class_section = f"{primary_child.current_class.name if primary_child and primary_child.current_class else ''} - {primary_child.current_section.name if primary_child and primary_child.current_section else ''}"
        
        parent_name = f"{parent.first_name} {parent.last_name}"
        children_names = ", ".join([f"{c.first_name} {c.last_name}" for c in children])
        
        row = [
            class_section,
            parent_name, parent.relationship, parent.phone_number, parent.address,
            children_names
        ]
        
        if include_credentials:
            if parent.user:
                if parent.user.initial_temp_password:
                    row.append(parent.user.initial_temp_password)
                else:
                    row.append("Already Set")
            else:
                row.append("No Account")
                
        writer.writerow(row)

    return response


@login_required
def reset_user_password(request, user_id):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission("dashboard.admin.view")):
            return JsonResponse({'success': False, 'error': 'Permission denied'})
        
        try:
            import string
            import random
            user = User.objects.get(pk=user_id)
            
            # Generate temporary password
            temp_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            user.set_password(temp_pass)
            user.initial_temp_password = temp_pass
            user.save()
            
            return JsonResponse({'success': True, 'temp_password': temp_pass})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request'})
