
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, StudentProfile
from app.models import Program


class LoginSerializer(TokenObtainPairSerializer):

    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id": str(self.user.id),
            "email": self.user.email,
            "role": self.user.role,
        }

        return data


class StudentCreateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"}
    )

    program = serializers.PrimaryKeyRelatedField(
        queryset=Program.objects.filter(is_active=True)
    )

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "email",
            "password",
            "program",
            "name",
            "roll_no",
            "phone",
            "image",
        ]

        read_only_fields = ["id"]

    @transaction.atomic
    def create(self, validated_data):

        email = validated_data.pop("email").lower()
        password = validated_data.pop("password")

        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({
                "email": "This email is already registered."
            })

        user = User.objects.create_user(
            email=email,
            password=password,
            role="STUDENT",
            is_active=True
        )

        student = StudentProfile.objects.create(
            user=user,
            **validated_data
        )

        return student


class StudentSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source="user.email", read_only=True)
    user_id = serializers.UUIDField(source="user.id", read_only=True)
    program_name = serializers.CharField(
        source="program.name",
        read_only=True
    )

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "user_id",
            "email",
            "program",
            "program_name",
            "name",
            "roll_no",
            "phone",
            "image",
            "created_at",
        ]

        read_only_fields = fields
