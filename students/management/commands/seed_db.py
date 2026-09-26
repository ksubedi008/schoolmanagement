import random
import datetime
import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from accounts.models import Role
from students.models import AcademicClass, Section, Student, Parent

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with realistic testing data (Classes, Sections, Students, Parents)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Data Arrays for authentic Nepali names
        male_first_names = [
            'Aarav', 'Bikash', 'Rabin', 'Sagar', 'Nabin', 'Ramesh', 'Sushil', 'Dipendra',
            'Prakash', 'Sunil', 'Bishal', 'Rajan', 'Kiran', 'Suman', 'Amrit', 'Sanjay',
            'Suresh', 'Bimal', 'Rupesh', 'Anil', 'Nitesh', 'Kamal', 'Krishna', 'Santosh'
        ]
        female_first_names = [
            'Aarti', 'Bipasha', 'Pooja', 'Sita', 'Gita', 'Nisha', 'Rupa', 'Smriti',
            'Kritika', 'Alina', 'Asmita', 'Sujata', 'Kopila', 'Sangita', 'Pratima',
            'Sarita', 'Manila', 'Anusha', 'Sabina', 'Susmita', 'Priyanka', 'Srijana'
        ]
        last_names = [
            'Thapa', 'Magar', 'Shrestha', 'Gurung', 'Tamang', 'Maharjan', 'Karki',
            'Khadka', 'Lama', 'Bhattarai', 'Sharma', 'Giri', 'Poudel', 'Adhikari',
            'Basnet', 'Gautam', 'Khatri', 'Rai', 'Limbu', 'Malla', 'Chaudhary', 'Yadav'
        ]
        addresses = [
            'Kathmandu', 'Pokhara', 'Lalitpur', 'Bhaktapur', 'Chitwan', 'Dharan',
            'Biratnagar', 'Butwal', 'Hetauda', 'Janakpur', 'Nepalgunj', 'Dhangadhi'
        ]
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

        # Ensure Roles exist
        student_role, _ = Role.objects.get_or_create(name='Student', defaults={'dashboard_redirect_url': '/dashboard/student/'})
        parent_role, _ = Role.objects.get_or_create(name='Parent', defaults={'dashboard_redirect_url': '/dashboard/parent/'})

        classes = ['Nursery', 'LKG', 'UKG'] + [f'Class {i}' for i in range(1, 11)]
        sections = ['A', 'B']

        total_students_created = 0
        total_parents_created = 0
        
        # Start admission number offset from the total number of students currently in DB
        db_student_count = Student.objects.count()

        # Create Classes and Sections
        for class_name in classes:
            academic_class, created = AcademicClass.objects.get_or_create(name=class_name)
            if created:
                self.stdout.write(f'Created Class: {class_name}')

            for section_name in sections:
                section, created = Section.objects.get_or_create(
                    academic_class=academic_class,
                    name=section_name
                )

                # Determine number of students for this section
                num_students = random.randint(35, 40)
                
                for roll in range(1, num_students + 1):
                    # 1. Generate Authentic Nepali Data
                    gender = random.choice(['M', 'F'])
                    if gender == 'M':
                        first_name = random.choice(male_first_names)
                    else:
                        first_name = random.choice(female_first_names)
                    
                    last_name = random.choice(last_names)
                    
                    admission_number = f"ADM{datetime.datetime.now().year}{(db_student_count + total_students_created + 1):05d}"
                    phone_number = f"98{random.randint(40000000, 69999999)}" # Starts with 984/985/986
                    address = f"{random.choice(addresses)}, Ward No. {random.randint(1, 15)}"
                    dob = datetime.date.today() - datetime.timedelta(days=random.randint(365 * 5, 365 * 16)) # Age 5 to 16

                    # 2. Create Student User Account
                    student_username = f"{first_name.lower()}.{admission_number.lower()}"
                    student_email = f"{student_username}@school.com"
                    
                    student_user = User.objects.create(
                        username=student_username,
                        email=student_email,
                        first_name=first_name,
                        last_name=last_name,
                        role=student_role,
                        phone_number=phone_number,
                        password=make_password('Student@123')
                    )

                    # Create Student Record
                    student = Student.objects.create(
                        user=student_user,
                        admission_number=admission_number,
                        roll_number=str(roll),
                        current_class=academic_class,
                        current_section=section,
                        first_name=first_name,
                        last_name=last_name,
                        date_of_birth=dob,
                        gender=gender,
                        blood_group=random.choice(blood_groups),
                        address=address,
                        phone_number=phone_number
                    )
                    total_students_created += 1

                    # 3. Parent / Sibling Logic
                    # 20% chance to reuse an existing parent (if one exists)
                    existing_parents = Parent.objects.all()
                    if random.random() < 0.2 and existing_parents.exists():
                        parent = random.choice(existing_parents)
                        # Optionally ensure they have the same last name (for realism)
                        parent.children.add(student)
                    else:
                        # 80% chance or fallback: Create a new Parent
                        parent_first = random.choice(male_first_names) # Defaulting to father
                        parent_last = last_name # Same as student
                        parent_phone = f"98{random.randint(40000000, 69999999)}"
                        parent_email = f"{parent_first.lower()}.{parent_last.lower()}{random.randint(10,99)}@gmail.com"
                        
                        parent_user = User.objects.create(
                            username=f"p_{student_username}",
                            email=parent_email,
                            first_name=parent_first,
                            last_name=parent_last,
                            role=parent_role,
                            phone_number=parent_phone,
                            password=make_password('Parent@123')
                        )
                        
                        parent = Parent.objects.create(
                            user=parent_user,
                            first_name=parent_first,
                            last_name=parent_last,
                            relationship='Father',
                            phone_number=parent_phone,
                            email=parent_email,
                            address=address,
                            occupation=random.choice(['Business', 'Teacher', 'Engineer', 'Doctor', 'Farmer', 'Govt Employee'])
                        )
                        parent.children.add(student)
                        total_parents_created += 1

                self.stdout.write(f'  - Populated Section {section_name} with {num_students} students.')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_students_created} Students and {total_parents_created} Parents across all classes.'))
