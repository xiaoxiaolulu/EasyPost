from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.service.https import ApiFastView
from api.service.project import (
    ProjectListViewSet,
    ProjectDestroyViewSet,
    ProjectUpdateViewSet,
    ProjectCreateViewSet,
    ProjectRetrieveApi
)
from api.service.user import CustomJsonWebToken

router = DefaultRouter()

app_urls = [
    # API
    path("", include(router.urls)),
    # API Authentication
    path("login/", CustomJsonWebToken.as_view()),

    path("http/", ApiFastView.as_view()),

    # 项目管理
    path("project/list", ProjectListViewSet.as_view()),
    path("project/delete/<int:pk>", ProjectDestroyViewSet.as_view()),
    path("project/update/<int:pk>", ProjectUpdateViewSet.as_view()),
    path("project/create", ProjectCreateViewSet.as_view()),
    path("prject/detail/<int:pk>", ProjectRetrieveApi.as_view())
]


# Final URL configuration
app_name = "api"
urlpatterns = app_urls + router.urls
