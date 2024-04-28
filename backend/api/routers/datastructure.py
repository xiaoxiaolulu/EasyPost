from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.service.setting import (
    DataStructureListViewSet,
    NoticeDestroyViewSet,
    DataSourceUpdateViewSet,
    DataSourceCreateViewSet
)


router = DefaultRouter()

app_urls = [
    path("list", DataStructureListViewSet.as_view()),
    path("delete/<int:pk>", NoticeDestroyViewSet.as_view()),
    path("update/<int:pk>", DataSourceUpdateViewSet.as_view()),
    path("create", DataSourceCreateViewSet.as_view())
]


app_name = RouterConfigEnum.DataStructure
urlpatterns = app_urls + router.urls
