from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models

from food_r.extensions.database.mixins import TimestampMixin


class User(AbstractBaseUser, TimestampMixin):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.email}"
