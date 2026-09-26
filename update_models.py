import os

file_path = 'students/models.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace AcademicClass subjects field
old_ac_field = "    subjects = models.ManyToManyField('Subject', related_name='classes', blank=True)"
new_ac_field = "    subjects = models.ManyToManyField('Subject', through='ClassSubject', related_name='classes', blank=True)"
content = content.replace(old_ac_field, new_ac_field)

# Add elective_subjects to Student
old_student_field = "    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')"
new_student_field = """    elective_subjects = models.ManyToManyField('Subject', related_name='elected_by_students', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')"""
content = content.replace(old_student_field, new_student_field)

addition = '''

class ClassSubject(models.Model):
    academic_class = models.ForeignKey(AcademicClass, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    subject_type = models.CharField(max_length=20, choices=[('COMPULSORY', 'Compulsory'), ('OPTIONAL', 'Optional')], default='COMPULSORY')
    
    class Meta:
        unique_together = ('academic_class', 'subject')

class ElectiveGroup(models.Model):
    academic_class = models.ForeignKey(AcademicClass, on_delete=models.CASCADE, related_name='elective_groups')
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField('Subject', related_name='elective_groups')
    
    def __str__(self):
        return f"{self.academic_class.name} - {self.name}"
'''

if 'class ClassSubject' not in content:
    content += addition
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Models updated.")
else:
    print("Models already updated.")
