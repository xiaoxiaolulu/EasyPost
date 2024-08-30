from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.service.user import (
    CustomJsonWebToken,
    UserListViewSet,
    UserRetrieveApi
)


router = DefaultRouter()

app_urls = [
    path("login/", CustomJsonWebToken.as_view()),
    path("list", UserListViewSet.as_view()),
    path("info", UserRetrieveApi.as_view())
]


app_name = RouterConfigEnum.USER
urlpatterns = app_urls + router.urls
