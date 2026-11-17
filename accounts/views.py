from django.shortcuts import render


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import StudentProfile
from .serializers import (
    LoginSerializer,
    StudentCreateSerializer,
    StudentSerializer,
)
from .permissions import IsAdminOrFaculty


class LoginView(TokenObtainPairView):

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]


class StudentViewSet(ModelViewSet):

    queryset = StudentProfile.objects.select_related(
        "user",
        "program"
    ).all().order_by("-created_at")

    permission_classes = [IsAdminOrFaculty]

    def get_serializer_class(self):

        if self.action == "create":
            return StudentCreateSerializer

        return StudentSerializer
