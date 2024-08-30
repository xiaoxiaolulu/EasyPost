from django.urls import path
from rest_framework.routers import DefaultRouter
from api.emus.RouterConfigEnum import RouterConfigEnum
from api.service.https import (
    DelApiView,
    ApiDetailView,
    SaveOrUpdateApiView,
    ApiSnapshotView,
    ApiTestListView,
    ImportApiView,
    RunApiView,
    ClosedTasksViewSet,
    ClosedTasksRetrieveApi
)


router = DefaultRouter()

app_urls = [
    path("delete/<int:pk>", DelApiView.as_view()),
    path("detail/<int:pk>", ApiDetailView.as_view()),
    path("saveOrUpdate/<int:pk>", SaveOrUpdateApiView.as_view()),
    path('snapshot', ApiSnapshotView.as_view()),
    path("list", ApiTestListView.as_view({'get': 'list'})),
    path("importApi/<int:pk>", ImportApiView.as_view()),
    path('run', RunApiView.as_view()),
    path("closedTasks", ClosedTasksViewSet.as_view()),
    path("closedTasks/detail/<int:pk>", ClosedTasksRetrieveApi.as_view())
]


app_name = RouterConfigEnum.HTTP
urlpatterns = app_urls + router.urls
