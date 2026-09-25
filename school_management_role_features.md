# School Management System
## Role-wise Responsibilities and Features

This document defines what each user type should be able to do in the School Management System.

### User Types

1. Admin
2. Principal
3. Vice Principal
4. Accountant
5. Librarian
6. Teacher
7. Class Teacher
8. Parent
9. Student

> **Design note:** A Class Teacher should normally be a Teacher with an additional class-teacher assignment, rather than a completely separate account role.



# 1. Admin

## User & Access Management
- Create users
- Edit users
- Activate/deactivate users
- Reset passwords
- Assign roles
- Manage permissions
- View login/activity history
- Manage account status

## Student Management
- Add students
- Edit student information
- View student profiles
- Assign class and section
- Assign roll number
- Assign admission number
- Transfer students
- Promote students
- Withdraw students
- Archive student records
- Manage student documents

## Parent Management
- Add parents/guardians
- Edit parent information
- Link parents to students
- Manage multiple children under one parent account
- Activate/deactivate parent accounts

## Teacher & Staff Management
- Add teachers/staff
- Edit staff information
- Assign subjects
- Assign classes/sections
- Assign class teachers
- Manage staff accounts
- View staff records

## Academic Configuration
- Create academic years
- Create classes
- Create sections
- Create subjects
- Configure grading systems
- Configure exam types
- Configure school terms
- Configure periods
- Configure school calendar

## System Management
- Manage school profile
- Manage school settings
- Manage notification settings
- Manage document templates
- Manage system-wide permissions
- View audit logs
- Generate system reports

## Dashboard
- View student statistics
- View teacher/staff statistics
- View attendance statistics
- View fee statistics
- View examination statistics
- View library statistics
- View system activity



# 2. Principal

## Dashboard & Monitoring
- View overall school statistics
- View student attendance
- View teacher attendance
- View academic performance
- View examination performance
- View fee collection reports
- View library reports
- View important notifications

## Student Management
- View student profiles
- View student academic history
- View student attendance
- View student performance
- View disciplinary records
- View student documents

## Teacher & Staff Management
- View teachers/staff
- View teacher attendance
- View teacher assignments
- View teacher workload
- Monitor academic activities

## Academic Management
- Monitor classes
- Monitor syllabus/academic progress
- View examination schedules
- View marks and results
- Review class performance
- Review subject performance
- Review student performance

## Approval & Administration
- Approve selected leave requests
- Approve selected academic requests
- Approve important notices
- Publish official announcements
- Review disciplinary cases
- Approve selected reports/documents

## Finance
- View financial reports
- View fee collection
- View outstanding fees
- View expenses
- View financial summaries

## Reports
- Student reports
- Attendance reports
- Academic reports
- Examination reports
- Teacher reports
- Financial reports
- School performance reports



# 3. Vice Principal

## Dashboard
- View school operational statistics
- View attendance
- View academic activities
- View teacher activities
- View important alerts

## Academic Monitoring
- Monitor classes
- Monitor teachers
- Monitor syllabus progress
- View examination progress
- View marks submission status
- Monitor result preparation

## Teacher Management
- View teacher assignments
- View teacher timetable
- View teacher attendance
- Monitor workload
- Coordinate teacher activities

## Student Management
- View student profiles
- View student attendance
- View academic performance
- View discipline records

## Attendance
- Monitor student attendance
- Monitor teacher attendance
- View attendance reports
- Follow up on unusual attendance patterns

## Timetable
- View class timetables
- View teacher timetables
- Coordinate timetable changes
- Manage/approve timetable adjustments where authorized

## Leave Management
- Review teacher leave requests
- Approve/reject teacher leave where authorized
- Monitor student leave requests
- Forward important requests to the Principal

## Examination
- Monitor exam preparation
- Monitor marks submission
- Review examination progress
- Review results before publication where authorized

## Communication
- Create announcements
- Send notices
- Communicate with teachers
- Communicate with relevant students/parents where authorized



# 4. Accountant

## Dashboard
- View today's collection
- View pending fees
- View overdue fees
- View monthly collection
- View expenses
- View financial summaries

## Fee Management
- Create fee structures
- Assign fees to classes/students
- View student fee accounts
- Collect fees
- Record payments
- Generate receipts
- Edit authorized transactions
- Process refunds where authorized
- Apply discounts where authorized
- Manage scholarships/concessions

## Payment Management
- Record cash payments
- Record bank payments
- Record online payments
- Track payment references
- View payment history
- Cancel/reverse transactions where authorized

## Outstanding Fees
- View unpaid fees
- View overdue fees
- Generate outstanding-fee reports
- Send fee reminders

## Expenses
- Record expenses
- Categorize expenses
- Upload expense documents
- View expense history
- Generate expense reports

## Financial Reports
- Daily collection report
- Monthly collection report
- Outstanding fee report
- Payment history
- Expense report
- Income/expense summary
- Student fee statement
- Receipt reports



# 5. Librarian

## Dashboard
- View total books
- View available books
- View issued books
- View overdue books
- View fines
- View recent transactions

## Book Management
- Add books
- Edit book information
- Archive books
- Manage ISBN
- Manage authors
- Manage publishers
- Manage categories
- Manage book copies
- Track book availability

## Issue & Return
- Issue books to students
- Issue books to teachers/staff if allowed
- Record returns
- Set due dates
- Renew books
- Calculate overdue fines
- Record lost/damaged books

## Member Management
- View student library accounts
- View teacher/staff library accounts
- View borrowed books
- View borrowing history

## Search
- Search books
- Search by title
- Search by author
- Search by ISBN
- Search by category
- Check availability

## Reports
- Issued books report
- Returned books report
- Overdue books report
- Fine report
- Lost/damaged books report
- Most borrowed books
- Member borrowing history



# 6. Teacher

## Dashboard
- View today's classes
- View assigned classes
- View assigned subjects
- View timetable
- View pending assignments
- View upcoming exams
- View notifications

## Student Management
- View students in assigned classes
- View student profiles
- View academic information
- View attendance
- View relevant student history

> Teachers should only see students/classes they are authorized to access.

## Attendance
- Mark student attendance
- Edit attendance within permitted time
- View attendance history
- View attendance reports
- Record present/absent/late/leave status

## Assignments & Homework
- Create assignments
- Add instructions
- Attach files
- Set due dates
- Edit assignments
- Delete/cancel assignments
- View submissions
- Grade submissions
- Give feedback

## Study Materials
- Upload notes
- Upload study materials
- Share links/resources
- Organize materials by class/subject

## Examination
- View exam schedule
- View assigned subjects
- Enter marks
- Edit marks before final submission
- Submit marks
- View submitted marks
- View student results where authorized

## Communication
- Send class-related announcements
- Communicate with students
- Communicate with parents where authorized
- Receive school notices

## Leave
- Apply for leave
- View leave status
- View leave history

## Timetable
- View personal timetable
- View assigned class timetable

---

# 7. Class Teacher

> A Class Teacher is a Teacher who has additional responsibility for a specific class/section.

## Everything a Teacher Can Do
- All regular teacher features
- Attendance
- Assignments
- Exams
- Marks
- Study materials
- Communication
- Personal timetable

## Class Management
- View all students in the assigned class
- View complete class attendance
- Monitor attendance trends
- View class performance
- Monitor assignments
- Monitor examination performance
- View class timetable

## Student Monitoring
- View student academic progress
- View student attendance history
- Monitor repeated absences
- View relevant discipline records
- Monitor student participation

## Parent Communication
- Communicate with parents of students in the assigned class
- Send class announcements
- Send attendance-related notifications where authorized
- Communicate about student academic concerns

## Leave Management
- Review student leave requests
- Approve/reject student leave where authorized
- Forward important requests to management

## Class Reports
- Generate class attendance reports
- Generate class performance reports
- Generate student summaries
- Generate class activity reports

## Class Administration
- Manage class notices
- Record class-related remarks
- Coordinate class activities
- Coordinate with subject teachers
- Report important issues to Vice Principal/Principal



# 8. Parent

## Dashboard
- View child/children overview
- View attendance
- View upcoming exams
- View assignments
- View fee status
- View notifications
- View school announcements

## Child Management
- View child's profile
- View class and section
- View roll number
- View academic information
- View school-related documents where available

## Attendance
- View daily attendance
- View monthly attendance
- View attendance percentage
- View absence history
- Receive attendance notifications where enabled

## Academic Performance
- View marks
- View grades
- View results
- View report cards
- View academic history

## Assignments
- View homework
- View assignments
- View due dates
- View submission status
- View teacher feedback

## Fees
- View fee structure
- View pending fees
- View paid fees
- View payment history
- View receipts
- Make online payments if payment gateway is enabled

## Library
- View borrowed books
- View due dates
- View overdue books
- View fines

## Leave
- Apply for child's leave
- View leave status
- View leave history

## Communication
- Receive school announcements
- Receive notices
- Receive notifications
- Communicate with class teacher where enabled

## Documents
- Download report cards
- Download receipts
- Download certificates/documents where authorized



# 9. Student

## Dashboard
- View today's timetable
- View upcoming classes
- View assignments
- View exams
- View attendance
- View results
- View notifications

## Profile
- View personal profile
- View class
- View section
- View roll number
- View admission number
- View assigned subjects

## Timetable
- View class timetable
- View subject schedule
- View examination timetable

## Attendance
- View personal attendance
- View attendance percentage
- View attendance history

## Assignments
- View assignments
- View instructions
- Download attachments
- Submit assignments
- View submission status
- View teacher feedback
- Resubmit where allowed

## Study Materials
- View class notes
- Download study materials
- Access shared resources

## Examination
- View exam schedule
- View subjects
- View marks
- View grades
- View results
- Download report cards

## Library
- Search books
- View available books
- View borrowed books
- View due dates
- View fines

## Leave
- Apply for leave where school policy permits
- View leave status
- View leave history

## Communication
- View school announcements
- View class announcements
- Receive notifications
- Receive teacher messages where enabled

---

# 10. Shared Features

These features can be available to multiple roles depending on permissions.

## Authentication
- Login
- Logout
- Forgot password
- Reset password
- Change password
- Profile management

## Notifications
- In-app notifications
- Email notifications
- SMS notifications (optional)
- Push notifications (optional)

## Search
- Search students
- Search teachers
- Search books
- Search classes
- Search records based on permissions

## Reports
- View reports
- Filter reports
- Export PDF
- Export Excel/CSV where authorized
- Print reports

## Audit & Security
- Record important system actions
- Track who created/edited/deleted records
- Track login activity
- Restrict unauthorized access



# 11. Important Permission Rules

The system should follow these principles:

### Admin
Full system configuration and user management.

### Principal
School-wide monitoring, approvals, and management.

### Vice Principal
Academic and operational coordination.

### Accountant
Financial operations only.

### Librarian
Library operations only.

### Teacher
Only assigned classes, subjects, and students.

### Class Teacher
Teacher permissions + additional access to their assigned class.

### Parent
Only their own children.

### Student
Only their own academic and school information.



# 12. Recommended Permission Model

Instead of checking only roles, use permissions.

Example:

```text
student.view
student.create
student.update
student.delete

attendance.view
attendance.create
attendance.update

exam.view
exam.create
exam.marks.enter
exam.marks.submit
exam.publish

fee.view
fee.collect
fee.refund

library.book.create
library.book.update
library.book.issue
library.book.return

assignment.create
assignment.update
assignment.grade

announcement.create
announcement.publish
```

Then attach permissions to roles.

This allows the school to customize permissions later without changing application code.



# 13. Scope-Based Access

Permissions should also have a scope.

For example:

```text
Teacher
    ↓
Computer
    ↓
Class 6A
Class 7A
Class 8B
```

The teacher can manage Computer-related activities for those classes, but not every class in the school.

A Class Teacher could have:

```text
Teacher
    +
Class Teacher
    ↓
Class 7A
```

A Parent:

```text
Parent
    ↓
Child A
Child B
```

A Student:

```text
Student
    ↓
Own Account
```

This prevents users from accessing information they should not see.



# 14. Future Features

These can be added after the core system is stable:

- Online admission
- Online fee payment
- SMS integration
- Email integration
- Push notifications
- Transport/bus management
- Hostel management
- Canteen management
- Payroll
- Inventory management
- Staff leave management
- School events
- Online classes
- Question bank
- Online examinations
- Certificates
- ID card generation
- QR-based attendance
- Biometric attendance integration
- Parent-teacher meeting scheduling
- Visitor management
- Complaint/feedback system
- Analytics dashboard
- Mobile application
