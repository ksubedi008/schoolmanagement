import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_management.settings")
django.setup()

from django.apps import apps
for model in apps.get_models():
    if model.__name__ == 'AcademicYear':
        print(f"Found in {model._meta.app_label}")
        print(model.objects.all().values('name', 'start_date', 'end_date'))
