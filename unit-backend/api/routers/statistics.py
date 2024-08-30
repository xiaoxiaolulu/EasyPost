from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.service.dashboard import StatisticsView


router = DefaultRouter()

app_urls = [
    path("summay", StatisticsView.as_view()),
]


app_name = RouterConfigEnum.STATISTICS
urlpatterns = app_urls + router.urls
