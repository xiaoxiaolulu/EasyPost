from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.views.https import (
    SaveOrUpdateCaseView,
    DelCaseView,
    CaseDetailView,
    CaseListView,
    RunCaseView,
    CaseStepDetailView,
    SaveOrUpdateStepView
)


router = DefaultRouter()

app_urls = [
    path("SaveOrUpdate/<int:pk>", SaveOrUpdateCaseView.as_view()),
    path('run', RunCaseView.as_view()),
    path('delete/<int:pk>', DelCaseView.as_view()),
    path('detail/<int:pk>', CaseDetailView.as_view()),
    path("list", CaseListView.as_view({'get': 'list'})),
    path('step/detail/<int:pk>', CaseStepDetailView.as_view()),
    path('step/saveOrUpdate/<int:pk>', SaveOrUpdateStepView.as_view())
]


app_name = RouterConfigEnum.CASE
urlpatterns = app_urls + router.urls
