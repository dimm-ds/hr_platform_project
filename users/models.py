from django.db import models
from django.contrib.auth.models import Permission, AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class Role(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


# Сигнал для создания ролей после миграций
@receiver(post_migrate)
def create_default_roles(**kwargs):

    # 1. Роль "candidate"
    candidate_role, c_created = Role.objects.get_or_create(name='candidate')
    if c_created:
        candidate_role.description = 'CRUD для своих резюме'
        crud_permissions = Permission.objects.filter(
            codename__in=['add_resume', 'change_resume', 'delete_resume', 'view_resume']
        )
        candidate_role.permissions.set(crud_permissions)
        candidate_role.save()

    # 2. Роль "HR Manager"
    hr_role, h_created = Role.objects.get_or_create(name='HR Manager')
    if h_created:
        hr_role.description = 'Только просмотр всех резюме'
        view_permission = Permission.objects.get(codename='view_resume')
        hr_role.permissions.set([view_permission])
        hr_role.save()

    # 3. Роль "admin"
    admin_role, a_created = Role.objects.get_or_create(name='admin')
    if a_created:
        admin_role.description = 'Полный доступ ко всему'
        all_permissions = Permission.objects.all()
        admin_role.permissions.set(all_permissions)
        admin_role.save()


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
