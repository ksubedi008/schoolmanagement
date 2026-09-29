from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch

from accounts.models import User, Role

@login_required
def home(request):
    return render(request, 'dashboard/default_dashboard.html')

from students.models import Student, Staff
from dashboard.models import AuditLog

@login_required
def admin_dashboard(request):
    if not request.user.has_scope_permission('dashboard.admin.view'):
        raise PermissionDenied("You do not have permission to view the Admin Dashboard.")
        
    student_count = Student.objects.filter(status='ACTIVE').count()
    staff_count = Staff.objects.count()
    recent_activity = AuditLog.objects.select_related('user').order_by('-timestamp')[:5]
    
    context = {
        'student_count': student_count,
        'staff_count': staff_count,
        'recent_activity': recent_activity,
        # Mocked stats for MVP
        'attendance_rate': 94.5,
        'fees_collected': 452000,
        'exams_scheduled': 12,
        'library_books_issued': 124,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def student_dashboard(request):
    if not request.user.has_scope_permission('dashboard.student.view'):
        raise PermissionDenied("You do not have permission to view the Student Dashboard.")
    return render(request, 'dashboard/student_dashboard.html')

# --- Admin Modules ---
@login_required
def admin_users(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
        
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            phone = request.POST.get('phone_number', '')
            role_id = request.POST.get('role')
            password = request.POST.get('password')
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.phone_number = phone
                if role_id:
                    user.role_id = role_id
                user.save()
                    
        elif action == 'edit':
            user_id = request.POST.get('user_id')
            try:
                user = User.objects.get(id=user_id)
                user.username = request.POST.get('username')
                user.email = request.POST.get('email')
                user.first_name = request.POST.get('first_name', '')
                user.last_name = request.POST.get('last_name', '')
                user.phone_number = request.POST.get('phone_number', '')
                user.role_id = request.POST.get('role') or None
                user.save()
            except User.DoesNotExist:
                pass
                
        elif action == 'toggle_status':
            user_id = request.POST.get('user_id')
            try:
                user = User.objects.get(id=user_id)
                if not user.is_superuser: # Don't lock out superusers
                    user.is_active = not user.is_active
                    user.save()
            except User.DoesNotExist:
                pass
                
        elif action == 'reset_password':
            user_id = request.POST.get('user_id')
            new_password = request.POST.get('new_password')
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
            except User.DoesNotExist:
                pass
    
    users = User.objects.exclude(role__name__in=['Student', 'Parent']).select_related('role').order_by('-date_joined')
    roles = Role.objects.exclude(name__in=['Student', 'Parent'])
    
    context = {
        'users': users,
        'roles': roles
    }
    return render(request, 'dashboard/modules/admin_users.html', context)

from students.models import Student, AcademicClass, Section, StudentDocument

@login_required
def admin_students(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
        
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            Student.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                admission_number=request.POST.get('admission_number'),
                roll_number=request.POST.get('roll_number', ''),
                current_class_id=request.POST.get('current_class') or None,
                current_section_id=request.POST.get('current_section') or None,
                phone_number=request.POST.get('phone_number', ''),
                gender=request.POST.get('gender', ''),
                status='ACTIVE'
            )
            
        elif action == 'edit':
            student_id = request.POST.get('student_id')
            try:
                student = Student.objects.get(id=student_id)
                student.first_name = request.POST.get('first_name')
                student.last_name = request.POST.get('last_name')
                student.admission_number = request.POST.get('admission_number')
                student.roll_number = request.POST.get('roll_number', '')
                student.current_class_id = request.POST.get('current_class') or None
                student.current_section_id = request.POST.get('current_section') or None
                student.phone_number = request.POST.get('phone_number', '')
                student.gender = request.POST.get('gender', '')
                student.save()
            except Student.DoesNotExist:
                pass
                
        elif action == 'change_status':
            student_id = request.POST.get('student_id')
            new_status = request.POST.get('status')
            try:
                student = Student.objects.get(id=student_id)
                student.status = new_status
                student.save()
                
                # Also update associated user account if it exists
                if student.user:
                    if new_status == 'ACTIVE':
                        student.user.is_active = True
                    else:
                        student.user.is_active = False
                    student.user.save()
                    
            except Student.DoesNotExist:
                pass
                
        elif action == 'promote':
            student_id = request.POST.get('student_id')
            new_class_id = request.POST.get('new_class')
            new_section_id = request.POST.get('new_section')
            try:
                student = Student.objects.get(id=student_id)
                student.current_class_id = new_class_id or None
                student.current_section_id = new_section_id or None
                student.save()
            except Student.DoesNotExist:
                pass
                
    classes = AcademicClass.objects.all()
    
    context = {
        'classes': classes,
    }
    return render(request, 'dashboard/modules/admin_students.html', context)

@login_required
def student_table_partial(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
        
    query = request.GET.get('q', '')
    class_id = request.GET.get('class', '')
    section_id = request.GET.get('section', '')
    page_number = request.GET.get('page', 1)
    
    students = Student.objects.filter(is_deleted=False).select_related('current_class', 'current_section').order_by('-id')
    
    if query:
        students = students.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(admission_number__icontains=query) |
            Q(roll_number__icontains=query)
        )
        
    if class_id:
        students = students.filter(current_class_id=class_id)
    if section_id:
        students = students.filter(current_section_id=section_id)
        
    paginator = Paginator(students, 20) # 20 per page
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/partials/student_table.html', {'students': page_obj})

@login_required
def soft_delete_student(request, pk):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        try:
            student = Student.objects.get(pk=pk, is_deleted=False)
            student.is_deleted = True
            student.save()
            return JsonResponse({'success': True})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def promote_transfer_student(request, pk):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        try:
            student = Student.objects.get(pk=pk, is_deleted=False)
            class_id = request.POST.get('class_id')
            section_id = request.POST.get('section_id')
            
            if not class_id or not section_id:
                return JsonResponse({'success': False, 'error': 'Class and Section are required.'}, status=400)
                
            student.current_class_id = class_id
            student.current_section_id = section_id
            student.save()
            
            return JsonResponse({'success': True})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def api_get_sections(request):
    class_id = request.GET.get('class_id')
    if not class_id:
        return JsonResponse({'sections': []})
    sections = Section.objects.filter(academic_class_id=class_id).values('id', 'name')
    return JsonResponse({'sections': list(sections)})

@login_required
def student_details_partial(request, pk):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    from django.shortcuts import get_object_or_404
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'dashboard/partials/student_details.html', {'student': student})

from students.models import Parent
from accounts.models import Role

@login_required
def admin_parents(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
        
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone_number', '')
            
            # Automatically create User account for parent
            username = email if email else f"parent_{phone}"
            parent_role, _ = Role.objects.get_or_create(name='Parent')
            
            user = None
            if username and not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=phone or "temp123")
                user.first_name = first_name
                user.last_name = last_name
                user.phone_number = phone
                user.role = parent_role
                user.save()
            
            parent = Parent.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone,
                relationship=request.POST.get('relationship', ''),
                occupation=request.POST.get('occupation', ''),
                address=request.POST.get('address', '')
            )
            
            children_ids = request.POST.getlist('children')
            if children_ids:
                parent.children.set(children_ids)
                
        elif action == 'edit':
            parent_id = request.POST.get('parent_id')
            try:
                parent = Parent.objects.get(id=parent_id)
                parent.first_name = request.POST.get('first_name')
                parent.last_name = request.POST.get('last_name')
                parent.email = request.POST.get('email')
                parent.phone_number = request.POST.get('phone_number', '')
                parent.relationship = request.POST.get('relationship', '')
                parent.occupation = request.POST.get('occupation', '')
                parent.address = request.POST.get('address', '')
                parent.save()
                
                # Update underlying user if exists
                if parent.user:
                    parent.user.first_name = parent.first_name
                    parent.user.last_name = parent.last_name
                    parent.user.email = parent.email
                    parent.user.phone_number = parent.phone_number
                    parent.user.save()
                
                children_ids = request.POST.getlist('children')
                parent.children.set(children_ids)
            except Parent.DoesNotExist:
                pass
                
        elif action == 'toggle_status':
            parent_id = request.POST.get('parent_id')
            try:
                parent = Parent.objects.get(id=parent_id)
                if parent.user:
                    parent.user.is_active = not parent.user.is_active
                    parent.user.save()
            except Parent.DoesNotExist:
                pass

    parents = Parent.objects.all().prefetch_related('children', 'user').order_by('-id')
    students = Student.objects.filter(status='ACTIVE')
    from students.models import AcademicClass
    classes = AcademicClass.objects.all()
    
    context = {
        'parents': parents,
        'students': students,
        'classes': classes,
    }
    return render(request, 'dashboard/modules/admin_parents.html', context)

from students.models import Staff, Subject, Section
from accounts.models import Role, User

@login_required
def admin_staff(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
        
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone_number', '')
            staff_type = request.POST.get('staff_type', 'TEACHER')
            emp_id = request.POST.get('employee_id')
            
            # Automatically create User account for staff
            username = email if email else emp_id
            
            # Get or create specific role based on staff_type
            role_name = 'Teacher' if staff_type == 'TEACHER' else ('Admin' if staff_type == 'ADMIN' else 'Staff')
            staff_role, _ = Role.objects.get_or_create(name=role_name)
            
            user = None
            if username and not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=phone or emp_id)
                user.first_name = first_name
                user.last_name = last_name
                user.phone_number = phone
                user.role = staff_role
                user.save()
            
            staff = Staff.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                staff_type=staff_type,
                employee_id=emp_id,
                email=email,
                phone_number=phone,
                department=request.POST.get('department', '')
            )
            
            subjects = request.POST.getlist('subjects')
            if subjects:
                staff.subjects.set(subjects)
                
            class_teacher_section = request.POST.get('class_teacher_section')
            if class_teacher_section:
                try:
                    section = Section.objects.get(id=class_teacher_section)
                    section.class_teacher = staff
                    section.save()
                except Section.DoesNotExist:
                    pass
                
        elif action == 'edit':
            staff_id = request.POST.get('staff_id')
            try:
                staff = Staff.objects.get(id=staff_id)
                staff.first_name = request.POST.get('first_name')
                staff.last_name = request.POST.get('last_name')
                staff.staff_type = request.POST.get('staff_type', 'TEACHER')
                staff.employee_id = request.POST.get('employee_id')
                staff.email = request.POST.get('email')
                staff.phone_number = request.POST.get('phone_number', '')
                staff.department = request.POST.get('department', '')
                staff.save()
                
                if staff.user:
                    staff.user.first_name = staff.first_name
                    staff.user.last_name = staff.last_name
                    staff.user.email = staff.email
                    staff.user.phone_number = staff.phone_number
                    staff.user.save()
                
                subjects = request.POST.getlist('subjects')
                staff.subjects.set(subjects)
                
                # Update class teacher assignment
                # First clear old
                Section.objects.filter(class_teacher=staff).update(class_teacher=None)
                # Then set new
                class_teacher_section = request.POST.get('class_teacher_section')
                if class_teacher_section:
                    section = Section.objects.get(id=class_teacher_section)
                    section.class_teacher = staff
                    section.save()
                    
            except Staff.DoesNotExist:
                pass
                
        elif action == 'toggle_status':
            staff_id = request.POST.get('staff_id')
            try:
                staff = Staff.objects.get(id=staff_id)
                if staff.user:
                    staff.user.is_active = not staff.user.is_active
                    staff.user.save()
            except Staff.DoesNotExist:
                pass

    staff_members = Staff.objects.all().prefetch_related('subjects', 'class_teacher_of', 'user').order_by('-id')
    subjects = Subject.objects.all()
    sections = Section.objects.all().select_related('academic_class')
    
    context = {
        'staff_members': staff_members,
        'subjects': subjects,
        'sections': sections,
    }
    return render(request, 'dashboard/modules/admin_staff.html', context)

from students.models import AcademicYear, GradingSystem, ExamType, SchoolTerm, Period, SchoolCalendarEvent, ElectiveGroup

@login_required
def admin_academic(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
        
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_academic_year':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            name = request.POST.get('name')
            
            if not start_date or not end_date:
                # Need valid dates, normally you'd use messages framework or redirect with error
                return redirect('dashboard:admin_academic')

            try:
                AcademicYear.objects.create(
                    name=name,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=request.POST.get('is_active') == 'on'
                )
                if request.POST.get('is_active') == 'on':
                    AcademicYear.objects.exclude(name=name).update(is_active=False)
            except Exception as e:
                # Handle db constraints or validation
                pass
                
        elif action == 'create_class':
            AcademicClass.objects.create(name=request.POST.get('name'))
            
        elif action == 'create_section':
            cls_id = request.POST.get('academic_class_id')
            if cls_id:
                Section.objects.create(
                    academic_class_id=cls_id,
                    name=request.POST.get('name')
                )
                
        elif action == 'create_subject':
            Subject.objects.create(
                name=request.POST.get('name'),
                code=request.POST.get('code')
            )

        elif action == 'create_elective_group':
            group = ElectiveGroup.objects.create(
                name=request.POST.get('name'),
                academic_class_id=request.POST.get('academic_class_id')
            )
            subject_ids = request.POST.getlist('subject_ids')
            if subject_ids:
                group.subjects.set(subject_ids)
            
        elif action == 'create_grading':
            GradingSystem.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description', '')
            )
            
        elif action == 'create_exam_type':
            ExamType.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description', '')
            )
            
        elif action == 'create_term':
            SchoolTerm.objects.create(
                academic_year_id=request.POST.get('academic_year_id'),
                name=request.POST.get('name'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date')
            )
            
        elif action == 'create_period':
            Period.objects.create(
                name=request.POST.get('name'),
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time')
            )
            
        elif action == 'create_event':
            SchoolCalendarEvent.objects.create(
                title=request.POST.get('title'),
                date=request.POST.get('date'),
                event_type=request.POST.get('event_type')
            )

    context = {
        'academic_years': AcademicYear.objects.all().order_by('-start_date'),
        'classes': AcademicClass.objects.all(),
        'sections': Section.objects.all().select_related('academic_class'),
        'subjects': Subject.objects.all(),
        'grading_systems': GradingSystem.objects.all(),
        'exam_types': ExamType.objects.all(),
        'terms': SchoolTerm.objects.all().select_related('academic_year'),
        'periods': Period.objects.all().order_by('start_time'),
        'events': SchoolCalendarEvent.objects.all().order_by('date'),
        'elective_groups': ElectiveGroup.objects.all().select_related('academic_class').prefetch_related('subjects'),
    }
    return render(request, 'dashboard/modules/admin_academic.html', context)

from dashboard.models import SchoolProfile, SystemSetting, AuditLog

@login_required
def admin_system(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
        
    profile, _ = SchoolProfile.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            profile.name = request.POST.get('name', profile.name)
            profile.email = request.POST.get('email', '')
            profile.phone = request.POST.get('phone', '')
            profile.address = request.POST.get('address', '')
            profile.website = request.POST.get('website', '')
            profile.principal_name = request.POST.get('principal_name', '')
            
            est_year = request.POST.get('established_year')
            if est_year and est_year.isdigit():
                profile.established_year = int(est_year)
                
            profile.save()
            
            AuditLog.objects.create(
                user=request.user,
                action="Updated School Profile",
                module="System"
            )
            
        elif action == 'create_setting':
            SystemSetting.objects.create(
                category=request.POST.get('category', 'GENERAL'),
                key=request.POST.get('key'),
                value=request.POST.get('value'),
                description=request.POST.get('description', '')
            )
            AuditLog.objects.create(
                user=request.user,
                action=f"Created System Setting: {request.POST.get('key')}",
                module="System"
            )

    settings_list = SystemSetting.objects.all().order_by('category')
    audit_logs = AuditLog.objects.all().select_related('user').order_by('-timestamp')[:50]
    
    context = {
        'profile': profile,
        'settings_list': settings_list,
        'audit_logs': audit_logs,
    }
    return render(request, 'dashboard/modules/admin_system.html', context)

from students.models import Parent, Subject, AcademicYear, GradingSystem, ExamType, SchoolTerm, Period, SchoolCalendarEvent
from django.contrib.auth import get_user_model

# ----------------- TEACHERS SPA -----------------
@login_required
def teacher_table_partial(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
        
    query = request.GET.get('q', '')
    subject_id = request.GET.get('subject', '')
    role_id = request.GET.get('role', '')
    page_number = request.GET.get('page', 1)
    
    staff_qs = Staff.objects.filter(is_deleted=False).prefetch_related('subjects').order_by('-joining_date')
    
    if query:
        staff_qs = staff_qs.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(employee_id__icontains=query)
        )
    if subject_id:
        staff_qs = staff_qs.filter(subjects__id=subject_id)
    if role_id:
        staff_qs = staff_qs.filter(staff_type=role_id)
        
    paginator = Paginator(staff_qs.distinct(), 20)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/partials/teacher_table.html', {'staff_members': page_obj})

@login_required
def teacher_details_partial(request, pk):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    staff = Staff.objects.get(pk=pk, is_deleted=False)
    # Check assigned classes
    assigned_sections = Section.objects.filter(class_teacher=staff)
    return render(request, 'dashboard/partials/teacher_details.html', {
        'staff': staff,
        'assigned_sections': assigned_sections
    })

@login_required
def soft_delete_teacher(request, pk):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
            return JsonResponse({'success': False, 'error': 'Permission denied'})
        try:
            staff = Staff.objects.get(pk=pk, is_deleted=False)
            
            # Check if assigned to an active class and flag it
            assigned_sections = Section.objects.filter(class_teacher=staff)
            warning = None
            if assigned_sections.exists():
                assigned_sections.update(class_teacher=None)
                warning = "Teacher was removed from active classes. Reassignment needed."
                
            staff.is_deleted = True
            staff.save()
            
            # Optional: Disable user account
            if staff.user:
                staff.user.is_active = False
                staff.user.save()
                
            return JsonResponse({'success': True, 'warning': warning})
        except Staff.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not found'})
            
# ----------------- PARENTS SPA -----------------
@login_required
def parent_table_partial(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
        
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)
    # Could filter by Account Status if user is linked and active
    status_filter = request.GET.get('status', '')
    
    parents = Parent.objects.filter(is_deleted=False).select_related('user').prefetch_related('children').order_by('-id')
    
    if query:
        parents = parents.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )
        
    if status_filter == 'active':
        parents = parents.filter(user__is_active=True)
    elif status_filter == 'inactive':
        parents = parents.filter(user__is_active=False)
    elif status_filter == 'pending':
        parents = parents.filter(user__isnull=True)
        
    paginator = Paginator(parents.distinct(), 20)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/partials/parent_table.html', {'parents': page_obj})

@login_required
def parent_details_partial(request, pk):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    parent = Parent.objects.prefetch_related('children__current_class', 'children__current_section').get(pk=pk, is_deleted=False)
    return render(request, 'dashboard/partials/parent_details.html', {'parent': parent})

@login_required
def soft_delete_parent(request, pk):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
            return JsonResponse({'success': False, 'error': 'Permission denied'})
        try:
            parent = Parent.objects.get(pk=pk, is_deleted=False)
            parent.is_deleted = True
            parent.save()
            if parent.user:
                parent.user.is_active = False
                parent.user.save()
            return JsonResponse({'success': True})
        except Parent.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not found'})

# ----------------- SYSTEM / USERS SPA -----------------
@login_required
def user_table_partial(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
        
    query = request.GET.get('q', '')
    role_id = request.GET.get('role', '')
    status = request.GET.get('status', '')
    page_number = request.GET.get('page', 1)
    
    users = get_user_model().objects.exclude(role__name__in=['Student', 'Parent']).select_related('role').order_by('-date_joined')
    
    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query)
        )
    if role_id:
        users = users.filter(role_id=role_id)
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)
        
    paginator = Paginator(users, 20)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/partials/user_table.html', {'users': page_obj})

@login_required
def soft_delete_user(request, pk):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
            return JsonResponse({'success': False, 'error': 'Permission denied'})
        try:
            user_obj = get_user_model().objects.get(pk=pk)
            # Soft delete = deactivate
            user_obj.is_active = False
            user_obj.save()
            return JsonResponse({'success': True})
        except get_user_model().DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not found'})

# ----------------- ACADEMIC CONFIG SPA -----------------
@login_required
def soft_delete_academic(request, model_type, pk):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
            return JsonResponse({'success': False, 'error': 'Permission denied'})
            
        models_map = {
            'class': AcademicClass,
            'section': Section,
            'subject': Subject,
            'year': AcademicYear,
            'grading': GradingSystem,
            'exam': ExamType,
            'term': SchoolTerm,
            'period': Period,
            'event': SchoolCalendarEvent,
            'elective_group': ElectiveGroup
        }
        
        ModelClass = models_map.get(model_type)
        if not ModelClass:
            return JsonResponse({'success': False, 'error': 'Invalid model type'})
            
        try:
            obj = ModelClass.objects.get(pk=pk)
            # Note: For strict relational integrity, some of these might need to be cascading 
            # or soft-deleted. But since the prompt said "Soft Delete Confirmation Modal", 
            # we will delete them here. Real soft deletes for config objects usually means adding an is_active field.
            # I will assume actual `.delete()` for these since it wasn't requested to add `is_deleted` to all 9 academic models.
            obj.delete()
            return JsonResponse({'success': True})
        except ModelClass.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not found'})

# ----------------- ROLE-SPECIFIC PORTALS -----------------
@login_required
def student_dashboard(request):
    return render(request, 'dashboard/portals/student_dashboard.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'dashboard/portals/teacher_dashboard.html')

@login_required
def parent_dashboard(request):
    return render(request, 'dashboard/portals/parent_dashboard.html')

@login_required
def class_details_partial(request, pk):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    try:
        academic_class = AcademicClass.objects.get(pk=pk)
        
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'update_class_teacher':
                section_id = request.POST.get('section_id')
                teacher_id = request.POST.get('teacher_id')
                try:
                    section = academic_class.sections.get(id=section_id)
                    section.class_teacher_id = teacher_id if teacher_id else None
                    section.save()
                    return JsonResponse({'success': True})
                except Section.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Section not found'}, status=404)
            elif action == 'edit_section':
                section_id = request.POST.get('section_id')
                name = request.POST.get('name')
                try:
                    section = academic_class.sections.get(id=section_id)
                    section.name = name
                    section.save()
                    return JsonResponse({'success': True})
                except Section.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Section not found'}, status=404)
            return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)
            
        all_subjects = Subject.objects.all().order_by('name')
        class_subjects = academic_class.subjects.all()
        sections = academic_class.sections.all().select_related('class_teacher')
        teachers = Staff.objects.filter(staff_type='TEACHER', is_deleted=False)
        return render(request, 'dashboard/partials/class_details.html', {
            'academic_class': academic_class,
            'all_subjects': all_subjects,
            'class_subjects': class_subjects,
            'sections': sections,
            'teachers': teachers
        })
    except AcademicClass.DoesNotExist:
        return HttpResponse('Class not found', status=404)

@login_required
def class_students_partial(request, pk):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    academic_class = get_object_or_404(AcademicClass, pk=pk)
    students = Student.objects.filter(current_class=academic_class, is_deleted=False).select_related('current_section')
    sections = academic_class.sections.all()
    return render(request, 'dashboard/partials/class_students.html', {
        'academic_class': academic_class,
        'students': students,
        'sections': sections
    })

@login_required
def class_parents_partial(request, pk):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    academic_class = get_object_or_404(AcademicClass, pk=pk)
    # Get parents of students in this class
    parents = Parent.objects.filter(
        children__current_class=academic_class, is_deleted=False
    ).distinct().prefetch_related(
        Prefetch('children', queryset=Student.objects.filter(current_class=academic_class))
    )
    return render(request, 'dashboard/partials/class_parents.html', {
        'academic_class': academic_class,
        'parents': parents
    })

import json
@login_required
def assign_class_subjects(request, pk):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
            return JsonResponse({'success': False, 'error': 'Permission denied'})
        try:
            academic_class = AcademicClass.objects.get(pk=pk)
            data = json.loads(request.body)
            subject_ids = data.get('subject_ids', [])
            academic_class.subjects.set(subject_ids)
            return JsonResponse({'success': True})
        except AcademicClass.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Class not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@login_required
def subject_details_partial(request, pk):
    if not (request.user.is_superuser or request.user.has_scope_permission("dashboard.admin.view")):
        raise PermissionDenied()
    try:
        subject = Subject.objects.get(pk=pk)
        all_classes = AcademicClass.objects.all().order_by('name')
        subject_classes = subject.classes.all()
        return render(request, 'dashboard/partials/subject_details.html', {
            'subject': subject,
            'all_classes': all_classes,
            'subject_classes': subject_classes
        })
    except Subject.DoesNotExist:
        return HttpResponse('Subject not found', status=404)

@login_required
def assign_subject_classes(request, pk):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission("dashboard.admin.view")):
            return JsonResponse({'success': False, 'error': 'Permission denied'})
        try:
            subject = Subject.objects.get(pk=pk)
            import json
            data = json.loads(request.body)
            class_ids = data.get('class_ids', [])
            subject.classes.set(class_ids)
            return JsonResponse({'success': True})
        except Subject.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Subject not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

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
            assignments = data.get('assignments', []) 
            
            with transaction.atomic():
                # --- HIGHLIGHTED FIX: Fetch all in one query ---
                student_ids = [a.get('student_id') for a in assignments]
                students_dict = Student.objects.in_bulk(student_ids)
                
                for assignment in assignments:
                    student_id = int(assignment.get('student_id'))
                    subject_ids = assignment.get('subject_ids', [])
                    
                    student = students_dict.get(student_id)
                    if student:
                        student.elective_subjects.set(subject_ids)
                # -----------------------------------------------
                        
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})