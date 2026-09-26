from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class AcademicClass(models.Model):
    name = models.CharField(max_length=50) # e.g. Class 1, Class 10
    subjects = models.ManyToManyField('Subject', through='ClassSubject', related_name='classes', blank=True)
    
    def __str__(self):
        return self.name

class Section(models.Model):
    academic_class = models.ForeignKey(AcademicClass, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=10) # e.g. A, B, C
    class_teacher = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='class_teacher_of')
    
    def clean(self):
        super().clean()
        if self.name:
            # Check for case-insensitive duplicate section names in the same class
            exists = Section.objects.filter(
                academic_class=self.academic_class,
                name__iexact=self.name
            ).exclude(pk=self.pk).exists()
            if exists:
                raise ValidationError({'name': 'A section with this name already exists in this class.'})

        if self.class_teacher:
            # Enforce strict One-to-One Class Teacher assignment
            is_assigned = Section.objects.filter(class_teacher=self.class_teacher).exclude(pk=self.pk).exists()
            if is_assigned:
                raise ValidationError({'class_teacher': 'This teacher is already assigned as a class teacher to another section.'})

    def __str__(self):
        return f"{self.academic_class.name} - {self.name}"

class Student(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('TRANSFERRED', 'Transferred'),
        ('WITHDRAWN', 'Withdrawn'),
        ('GRADUATED', 'Graduated'),
        ('ARCHIVED', 'Archived'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profile')
    
    # Academic Info
    admission_number = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=10, blank=True)
    current_class = models.ForeignKey(AcademicClass, on_delete=models.SET_NULL, null=True, blank=True)
    current_section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    
    # Contact Info
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Status
    elective_subjects = models.ManyToManyField('Subject', related_name='elected_by_students', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    admission_date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.admission_number})"

class StudentDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='student_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.student.first_name}"

class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='parent_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50, blank=True) # Father, Mother, Guardian
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    
    # Managing multiple children under one account
    children = models.ManyToManyField(Student, related_name='parents', blank=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.name

class Staff(models.Model):
    STAFF_TYPES = [
        ('TEACHER', 'Teacher'),
        ('ADMIN', 'Administrative'),
        ('SUPPORT', 'Support Staff')
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPES, default='TEACHER')
    employee_id = models.CharField(max_length=50, unique=True)
    
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    joining_date = models.DateField(auto_now_add=True)
    
    # Assignments (for teachers)
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

class AcademicYear(models.Model):
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class GradingSystem(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class ExamType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class SchoolTerm(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='terms')
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.academic_year.name} - {self.name}"

class Period(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return self.name

class SchoolCalendarEvent(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    event_type = models.CharField(max_length=50, choices=[('HOLIDAY', 'Holiday'), ('EXAM', 'Exam'), ('EVENT', 'School Event')])
    
    def __str__(self):
        return f"{self.title} on {self.date}"


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
