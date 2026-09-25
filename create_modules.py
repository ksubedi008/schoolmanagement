import os

base_dir = r'c:\Kamal\Project\schoolmanagement\templates\dashboard\modules'
os.makedirs(base_dir, exist_ok=True)

modules = [
    ('admin_users.html', 'User & Access Management', 'Manage roles, passwords, and system access.'),
    ('admin_students.html', 'Student Management', 'Manage student admissions, profiles, and promotions.'),
    ('admin_parents.html', 'Parent Management', 'Manage parent accounts and link them to students.'),
    ('admin_staff.html', 'Teacher & Staff Management', 'Manage staff records, subjects, and workloads.'),
    ('admin_academic.html', 'Academic Configuration', 'Configure terms, classes, subjects, and grading.'),
    ('admin_system.html', 'System Management', 'Manage global settings, backups, and notifications.')
]

template = """{% extends 'layout.html' %}

{% block title %}{title} | SMS{% endblock %}
{% block page_title %}{title}{% endblock %}

{% block content %}
<div class="card">
    <h3 class="card-title">{title}</h3>
    <p style="color: var(--text-secondary); margin-top: 1rem;">{desc}</p>
    
    <div style="margin-top: 2rem; padding: 2rem; border: 2px dashed var(--border-color); border-radius: 8px; text-align: center; color: var(--text-secondary);">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom: 1rem;"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        <h4>Module Under Construction</h4>
        <p>This module's interface is currently being built.</p>
        <br>
        <a href="{% url 'dashboard:admin_dashboard' %}" class="btn" style="background: var(--primary-color); color: white; text-decoration: none; padding: 0.75rem 1.5rem; border-radius: 8px; display: inline-block; margin-top: 1rem;">Return to Admin Overview</a>
    </div>
</div>
{% endblock %}
"""

for filename, title, desc in modules:
    with open(os.path.join(base_dir, filename), 'w') as f:
        f.write(template.format(title=title, desc=desc))

print('Created templates successfully.')
