from django.db.models import Count
from .models import Group


def adding_student_to_group(product, user):
    '''
    Добавляем студента в группу, где не превышен лимит. 
    '''
    groups = Group.objects.filter(product=product).annotate(students_number=Count('students'))
    target_groups = groups.filter(students_number__lt=product.max_users)

    if target_groups:
        for group in target_groups:
            group.students.add(user)
            return group
    return None
