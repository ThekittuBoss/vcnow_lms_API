
from rest_framework.viewsets import ModelViewSet

from .models import Program
from .serializers import ProgramSerializer
from accounts.permissions import IsAdminOrFaculty


class ProgramViewSet(ModelViewSet):

    queryset = Program.objects.all().order_by("-created_at")
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminOrFaculty]
