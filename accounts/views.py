from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def traffic_control(request):
    """
    Central traffic-control view that redirects users to their specific 
    dashboards based on their assigned role's dashboard_redirect_url.
    Avoids hardcoding specific roles (e.g., if user.is_teacher).
    """
    if request.user.is_superuser:
        return redirect('dashboard:admin_dashboard')
    
    if request.user.role and request.user.role.dashboard_redirect_url:
        return redirect(request.user.role.dashboard_redirect_url)
    
    # Fallback dashboard
    return redirect('dashboard:home')
