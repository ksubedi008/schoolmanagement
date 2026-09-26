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

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('dashboard:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Clear the temporary password once changed
        if self.request.user.initial_temp_password:
            self.request.user.initial_temp_password = ''
            self.request.user.save(update_fields=['initial_temp_password'])
        return response
