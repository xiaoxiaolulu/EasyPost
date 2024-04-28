from django.urls import path
from rest_framework.routers import DefaultRouter
from api.service.user import (
    CustomJsonWebToken,
    UserListViewSet
)


router = DefaultRouter()

app_urls = [
    path("login/", CustomJsonWebToken.as_view()),
    path("list", UserListViewSet.as_view()),
]


app_name = "user"
urlpatterns = app_urls + router.urls
