from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.service.project import (
    ProjectListViewSet,
    ProjectDestroyViewSet,
    ProjectUpdateViewSet,
    ProjectCreateViewSet,
    ProjectRetrieveApi,
    ProjectRoleDestroyViewSet,
    ProjectRoleUpdateViewSet
)


router = DefaultRouter()

app_urls = [
    path("list", ProjectListViewSet.as_view()),
    path("delete/<int:pk>", ProjectDestroyViewSet.as_view()),
    path("update/<int:pk>", ProjectUpdateViewSet.as_view()),
    path("create", ProjectCreateViewSet.as_view()),
    path("detail/<int:pk>", ProjectRetrieveApi.as_view()),
    path("role/delete", ProjectRoleDestroyViewSet.as_view()),
    path("role/add", ProjectRoleUpdateViewSet.as_view()),
]


app_name = RouterConfigEnum.PROJECT
urlpatterns = app_urls + router.urls
