"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.global_settings import MEDIA_ROOT
from django.contrib import admin
from django.urls import (
    path,
    include,
    re_path
)
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

swagger_info = openapi.Info(
    title="EasyPost API",
    default_version='v1',
    description="""EasyPost.

The `swagger-ui` view can be found [here](/swagger).
The `ReDoc` view can be found [here](/redoc).
The swagger YAML document can be found [here](/swagger/?format=openapi).

You can log in using the pre-existing `admin` user with password `passwordadmin`.""",  # noqa
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@snippets.local"),
    license=openapi.License(name="BSD License"),
)

SchemaView = get_schema_view(
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # Site Authentication
    path("auth/", include("rest_framework.urls")),
    # Admin
    path("admin/", admin.site.urls),
    # User
    path("api/user/", include("api.routers.user", "user")),
    # Statistics
    path("api/statistics/", include("api.routers.statistics", "statistics")),
    # Project
    path("api/project/", include("api.routers.project", "project")),
    # Env
    path("api/env/", include("api.routers.env", "env")),
    # Database
    path("api/database/", include("api.routers.database", "database")),
    # Function
    path("api/function/", include("api.routers.function", "function")),
    # Notice
    path("api/notice/", include("api.routers.notice", "notice")),
    # Tree
    path("api/tree/", include("api.routers.tree", "tree")),
    # Http
    path("api/http/", include("api.routers.http", "http")),
    # Case
    path("api/case/", include("api.routers.case", "case")),
    # Plan
    path("api/plan/", include("api.routers.plan", "plan")),
    # Report
    path("api/report/", include("api.routers.report", "report")),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    re_path(r'^swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
