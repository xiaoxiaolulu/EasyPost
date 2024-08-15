from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.service.setting import (
    TestEnvironmentListViewSet,
    TestEnvironmentDestroyViewSet,
    EnvironmentSaveOrUpdateApiView,
    EnvironmentDetailView
)


router = DefaultRouter()

app_urls = [
    path("list", TestEnvironmentListViewSet.as_view()),
    path("delete/<int:pk>", TestEnvironmentDestroyViewSet.as_view()),
    path("saveOrUpdate/<int:pk>", EnvironmentSaveOrUpdateApiView.as_view()),
    path("detail/<int:pk>", EnvironmentDetailView.as_view())
]


app_name = RouterConfigEnum.ENV
urlpatterns = app_urls + router.urls
