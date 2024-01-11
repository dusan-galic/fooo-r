from typing import List

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls.conf import include, path
from drf_yasg import openapi, views
from rest_framework import permissions

schema_view = views.get_schema_view(
    openapi.Info(
        title="Food recipes",
        description="FOOD-R Backend API",
        default_version="1.0.0",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns: List = [
    path("api/", include("food_r.modules.users.api.urls")),
    path("api/", include("food_r.modules.recipes.api.urls")),
    path(
        "api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"
    ),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
]
# Add static files to `urlpatterns`.
urlpatterns += staticfiles_urlpatterns()
