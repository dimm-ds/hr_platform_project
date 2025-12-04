from rest_framework import serializers
from django.contrib.auth.models import Permission
from .models import User, Role


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        role, created = Role.objects.get_or_create(name="candidate")
        if created:
            role.description = 'CRUD'
            role.save()
            crud_permissions = Permission.objects.filter(
                content_type__app_label='resumes',
                content_type__model='resume',
                codename__in=['add_resume', 'change_resume', 'delete_resume', 'view_resume']
            )

            print(f"Найдено прав: {crud_permissions.count()}")
            for p in crud_permissions:
                print(f"  - {p.codename}")

            role.permissions.set(crud_permissions)
        user.role = role
        user.save()
        return user
