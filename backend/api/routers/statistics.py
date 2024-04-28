from django.urls import path
from rest_framework.routers import DefaultRouter
from api.service.dashboard import StatisticsView


router = DefaultRouter()

app_urls = [
    path("summay", StatisticsView.as_view()),
]


app_name = "statistics"
urlpatterns = app_urls + router.urls
