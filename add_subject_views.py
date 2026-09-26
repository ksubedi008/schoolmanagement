import sys

file_path = 'dashboard/views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

addition = '''
@login_required
def subject_details_partial(request, pk):
    if not (request.user.is_superuser or request.user.has_scope_permission("dashboard.admin.view")):
        raise PermissionDenied()
    try:
        subject = Subject.objects.get(pk=pk)
        all_classes = AcademicClass.objects.all().order_by('name')
        subject_classes = subject.classes.all()
        return render(request, 'dashboard/partials/subject_details.html', {
            'subject': subject,
            'all_classes': all_classes,
            'subject_classes': subject_classes
        })
    except Subject.DoesNotExist:
        return HttpResponse('Subject not found', status=404)

@login_required
def assign_subject_classes(request, pk):
    if request.method == 'POST':
        if not (request.user.is_superuser or request.user.has_scope_permission("dashboard.admin.view")):
            return JsonResponse({'success': False, 'error': 'Permission denied'})
        try:
            subject = Subject.objects.get(pk=pk)
            import json
            data = json.loads(request.body)
            class_ids = data.get('class_ids', [])
            subject.classes.set(class_ids)
            return JsonResponse({'success': True})
        except Subject.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Subject not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
'''

if 'def subject_details_partial' not in content:
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(addition)
    print('Added successfully')
else:
    print('Already added')
