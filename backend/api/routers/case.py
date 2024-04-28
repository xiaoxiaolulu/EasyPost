from django.urls import path
from rest_framework.routers import DefaultRouter
from api.service.https import (
    SaveOrUpdateCaseView,
    DelCaseView,
    CaseDetailView,
    CaseListView,
    RunCaseView
)


router = DefaultRouter()

app_urls = [
    path("SaveOrUpdate/<int:pk>", SaveOrUpdateCaseView.as_view()),
    path('run', RunCaseView.as_view()),
    path('delete/<int:pk>', DelCaseView.as_view()),
    path('detail/<int:pk>', CaseDetailView.as_view()),
    path("list", CaseListView.as_view({'get': 'list'})),
]


app_name = "case"
urlpatterns = app_urls + router.urls
