from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.service.plan import (
    SaveOrUpdatePlanView,
    UpdatePlanStateView,
    RunPlanView,
    DelPlanView,
    PlanDetailView,
    PlanListViewSet,
    ApschedulerJobsListViewSet
)


router = DefaultRouter()

app_urls = [
    path("SaveOrUpdate/<int:pk>", SaveOrUpdatePlanView.as_view()),
    path("UpdatePlanState/<int:task_id>/<int:target_status>", UpdatePlanStateView.as_view()),
    path("run", RunPlanView.as_view()),
    path('delete/<int:pk>', DelPlanView.as_view()),
    path('detail/<int:pk>', PlanDetailView.as_view()),
    path("list", PlanListViewSet.as_view()),
    path("record/list", ApschedulerJobsListViewSet.as_view())
]


app_name = RouterConfigEnum.PLAN
urlpatterns = app_urls + router.urls
