from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from accounts.models import User, Role

@login_required
def home(request):
    return render(request, 'dashboard/default_dashboard.html')

@login_required
def admin_dashboard(request):
    if not request.user.has_scope_permission('dashboard.admin.view'):
        raise PermissionDenied("You do not have permission to view the Admin Dashboard.")
    return render(request, 'dashboard/admin_dashboard.html')

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
    
    users = User.objects.all().select_related('role').order_by('-date_joined')
    roles = Role.objects.all()
    
    context = {
        'users': users,
        'roles': roles
    }
    return render(request, 'dashboard/modules/admin_users.html', context)

@login_required
def admin_students(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    return render(request, 'dashboard/modules/admin_students.html')

@login_required
def admin_parents(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    return render(request, 'dashboard/modules/admin_parents.html')

@login_required
def admin_staff(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    return render(request, 'dashboard/modules/admin_staff.html')

@login_required
def admin_academic(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    return render(request, 'dashboard/modules/admin_academic.html')

@login_required
def admin_system(request):
    if not (request.user.is_superuser or request.user.has_scope_permission('dashboard.admin.view')):
        raise PermissionDenied()
    return render(request, 'dashboard/modules/admin_system.html')

