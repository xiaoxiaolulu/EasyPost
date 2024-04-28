from django.urls import path
from rest_framework.routers import DefaultRouter
from api.service.report import (
    ReportDetailView,
    ReportListViewSet
)


router = DefaultRouter()

app_urls = [
    path("detail", ReportDetailView.as_view({'get': 'list'})),
    path("list", ReportListViewSet.as_view())
]


app_name = "report"
urlpatterns = app_urls + router.urls
