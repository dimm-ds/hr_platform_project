from rest_framework.permissions import BasePermission, SAFE_METHODS


class ResumePermission(BasePermission):
    def has_permission (self, request, view):
        user = request.user

        if not user.is_authenticated or not user.role:
            return False
        action_to_permission = {
            'list': 'view_resume',
            'retrieve': 'view_resume',
            'create': 'add_resume',
            'update': 'change_resume',
            'partial_update': 'change_resume',
            'destroy': 'delete_resume',
        }

        required_perm = action_to_permission.get(view.action)

        return request.user.role.permissions.filter(
            codename=required_perm
        ).exists()

