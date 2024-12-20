from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.views.setting import (
    NoticeListViewSet,
    NoticeDestroyViewSet,
    NoticeDetailView,
    NoticeSaveOrUpdateApiView
)


router = DefaultRouter()

app_urls = [
    path("list", NoticeListViewSet.as_view()),
    path("delete/<int:pk>", NoticeDestroyViewSet.as_view()),
    path("detail/<int:pk>", NoticeDetailView.as_view()),
    path("saveOrUpdate/<int:pk>", NoticeSaveOrUpdateApiView.as_view()),
]


app_name = RouterConfigEnum.NOTICE
urlpatterns = app_urls + router.urls
