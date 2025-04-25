from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path

from cooking import views


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Документация по API к ресурсу кулинария",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # SWAGGER
    
    # 1 вариант
    path("swagger-ui/", views.SwaggerApiDoc.as_view(), name="swagger-ui"),
    path("openapi", schema_view.as_view(), name="openapi-schema"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.with_ui(cache_timeout=1),
        name="schema-json",
    ),
    # 2 вариант
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
