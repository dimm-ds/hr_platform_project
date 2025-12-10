from rest_framework import viewsets
from .permissions import ResumePermission
from .models import Resume
from .serializers import ResumeSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    permission_classes = [ResumePermission]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Resume.objects.none()

        user = self.request.user

        if user.is_superuser or user.role.name in ('HR Manager', 'admin'):
            return Resume.objects.all()

        return Resume.objects.filter(user=user)