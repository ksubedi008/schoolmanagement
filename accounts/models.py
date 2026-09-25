from django.db import models
from django.contrib.auth.models import AbstractUser

class Permission(models.Model):
    """
    Granular permissions string, e.g., 'student.view', 'exam.marks.enter'
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    """
    A Role aggregates multiple permissions and is assigned to a User.
    e.g., Admin, Principal, Teacher, Student
    """
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name="roles")
    dashboard_redirect_url = models.CharField(max_length=255, default='/dashboard/', help_text="URL to redirect to upon login")

    def __str__(self):
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    phone_number = models.CharField(max_length=20, blank=True)

    def has_scope_permission(self, perm_name):
        """
        Checks if the user has a specific granular permission through their role.
        Superusers have all permissions.
        """
        if self.is_superuser:
            return True
        if self.role:
            return self.role.permissions.filter(name=perm_name).exists()
        return False
