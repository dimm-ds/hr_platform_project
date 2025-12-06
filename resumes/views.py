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

        user = self.request.user


        # Super admin и HR видят всё
        if user.is_superuser or user.role.name in ('HR Manager', 'admin'):
            return Resume.objects.all()

        # Users видят только свои
        return Resume.objects.filter(user=user)