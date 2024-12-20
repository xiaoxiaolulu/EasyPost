from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.views.setting import (
    DataSourceListViewSet,
    DataSourceDestroyViewSet,
    DataSourceUpdateViewSet,
    DataSourceCreateViewSet,
    DatabaseIsConnectView
)


router = DefaultRouter()

app_urls = [
    path("list", DataSourceListViewSet.as_view()),
    path("delete/<int:pk>", DataSourceDestroyViewSet.as_view()),
    path("update/<int:pk>", DataSourceUpdateViewSet.as_view()),
    path("create", DataSourceCreateViewSet.as_view()),
    path("isConnect", DatabaseIsConnectView.as_view()),
]


app_name = RouterConfigEnum.DATABASE
urlpatterns = app_urls + router.urls
