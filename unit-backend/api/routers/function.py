from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.views.setting import (
    FunctionsListViewSet,
    DebugFunctionApiView,
    GetFunctionListApiView,
    FunctionSaveOrUpdateApiView
)


router = DefaultRouter()

app_urls = [
    path("saveOrUpdate/<int:pk>", FunctionSaveOrUpdateApiView.as_view()),
    path("detailList", GetFunctionListApiView.as_view()),
    path("debug/<int:pk>", DebugFunctionApiView.as_view()),
    path("list", FunctionsListViewSet.as_view()),
]


app_name = RouterConfigEnum.FUNCTION
urlpatterns = app_urls + router.urls
