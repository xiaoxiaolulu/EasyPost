from django.urls import path
from rest_framework.routers import DefaultRouter
from api.service.setting import (
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


app_name = "function"
urlpatterns = app_urls + router.urls
