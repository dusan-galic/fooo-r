from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from food_r.modules.users.models import User


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
        )


class CreateUserSerializer(UserBaseSerializer):
    class Meta:
        model = User
        fields = UserBaseSerializer.Meta.fields + ("password",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class AuthUserSerializer(TokenObtainPairSerializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("refresh", "access")


class AuthUserResponseSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("refresh", "access")
