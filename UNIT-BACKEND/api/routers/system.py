from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.service.system import MenuView


router = DefaultRouter()

app_urls = [
    path("menu", MenuView.as_view()),
]


app_name = RouterConfigEnum.NOTICE
urlpatterns = app_urls + router.urls
