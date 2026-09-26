import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from students.models import AcademicClass, Student

with open('db_report.txt', 'w') as f:
    classes = AcademicClass.objects.all().order_by('id')
    total = 0
    for c in classes:
        count = Student.objects.filter(current_class=c).count()
        f.write(f"{c.name}: {count} students\n")
        total += count
    f.write(f"Total students across all classes: {total}\n")
