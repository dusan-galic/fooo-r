from typing import List

from django.urls.conf import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from food_r.modules.users.api.views import UserLoginView, UserRegistrationView

router = SimpleRouter()
router.register(
    r"user/registration", UserRegistrationView, basename="user_registration"
)

urlpatterns: List = [
    path("user/login", UserLoginView.as_view(), name="user_login"),
    path("user/refresh", TokenRefreshView.as_view(), name="user_refresh"),
]
urlpatterns += router.urls
