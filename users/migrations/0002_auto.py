from django.db import migrations


def create_default_roles(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    Permission = apps.get_model('auth', 'Permission')

    from django.contrib.auth.management import create_permissions
    from django.apps import apps as django_apps

    resumes_app = django_apps.get_app_config('resumes')
    create_permissions(resumes_app, verbosity=0)

    # candidate
    candidate_role, created = Role.objects.get_or_create(name='candidate')
    if created:
        candidate_role.description = 'CRUD для своих резюме'
        candidate_role.save()

        candidate_perms = Permission.objects.filter(
            codename__in=['add_resume', 'change_resume', 'delete_resume', 'view_resume']
        )
        candidate_role.permissions.add(*candidate_perms)

    # HR Manager
    hr_role, created = Role.objects.get_or_create(name='HR Manager')
    if created:
        hr_role.description = 'Только просмотр всех резюме'
        hr_role.save()

        view_perm = Permission.objects.filter(codename='view_resume').first()
        hr_role.permissions.add(view_perm)

    # admin
    admin_role, created = Role.objects.get_or_create(name='admin')
    if created:
        admin_role.description = 'Полный доступ ко всему'
        admin_role.save()

        all_perms = Permission.objects.all()
        admin_role.permissions.add(*all_perms)


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
        ('resumes', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_default_roles)
    ]