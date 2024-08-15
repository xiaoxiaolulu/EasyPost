from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.service.https import (
    TreeView
)


router = DefaultRouter()

app_urls = [
    path("<int:pk>&<int:use_type>", TreeView.as_view()),
]


app_name = RouterConfigEnum.TREE
urlpatterns = app_urls + router.urls
