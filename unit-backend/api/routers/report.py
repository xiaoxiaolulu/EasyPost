from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.views.report import (
    ReportDetailView,
    ReportListViewSet
)


router = DefaultRouter()

app_urls = [
    path("detail", ReportDetailView.as_view({'get': 'list'})),
    path("list", ReportListViewSet.as_view())
]


app_name = RouterConfigEnum.REPORT
urlpatterns = app_urls + router.urls
