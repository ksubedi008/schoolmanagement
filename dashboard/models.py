from django.db import models
from django.conf import settings

class SchoolProfile(models.Model):
    name = models.CharField(max_length=200, default='My School')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    principal_name = models.CharField(max_length=100, blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class SystemSetting(models.Model):
    category = models.CharField(max_length=50, choices=[
        ('GENERAL', 'General'),
        ('NOTIFICATION', 'Notification'),
        ('PERMISSION', 'Permissions')
    ], default='GENERAL')
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.key}: {self.value}"

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=200)
    module = models.CharField(max_length=50) # e.g. Students, Parents, Staff
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"
