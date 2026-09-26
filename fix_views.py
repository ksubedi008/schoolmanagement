import sys

file_path = 'dashboard/views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'parents = parents.filter(user__isnull=True)' in line:
        new_lines.append('        \n')
        new_lines.append('    class_id = request.GET.get("class_id")\n')
        new_lines.append('    section_id = request.GET.get("section_id")\n')
        new_lines.append('    if class_id:\n')
        new_lines.append('        parents = parents.filter(children__current_class_id=class_id)\n')
        new_lines.append('    if section_id:\n')
        new_lines.append('        parents = parents.filter(children__current_section_id=section_id)\n')

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done replacing.")
