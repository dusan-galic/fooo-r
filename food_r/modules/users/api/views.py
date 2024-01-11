import requests
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from food_r.modules.users.api.serializers import (
    AuthUserResponseSerializer,
    AuthUserSerializer,
    CreateUserSerializer,
    UserBaseSerializer,
)
from food_r.modules.users.models import User
from food_r.settings.consts import HUNTER_API_KEY, HUNTER_URL


class UserRegistrationView(CreateModelMixin, GenericViewSet):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Check if email exist.
        response = requests.get(
            f"{HUNTER_URL}email-verifier?email={validated_data['email']}&api_key={HUNTER_API_KEY}"
        )
        if response.status_code != HTTP_200_OK:
            raise Exception(response)
        if response.json()["data"]["status"] == "invalid":
            raise ValidationError("Email does not exist.")

        validated_data["password"] = make_password(validated_data["password"])
        user = User.objects.create(**validated_data)
        user_data = UserBaseSerializer(user).data

        return Response(user_data, status=status.HTTP_201_CREATED)


class UserLoginView(TokenObtainPairView):
    """Takes a set of user credentials and returns access and refresh JWT pair
    to prove the authentication of those credentials.

    post:
        Logins user by providing Json Web Token (JWT)
    """

    serializer_class = AuthUserSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: AuthUserResponseSerializer})
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)
