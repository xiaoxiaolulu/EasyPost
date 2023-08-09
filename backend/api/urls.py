from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.service.https import ApiFastView
from api.service.project import ProjectViewSet, ProjectListViewSet
from api.service.user import CustomJsonWebToken

router = DefaultRouter()

router.register('project', ProjectViewSet)


app_urls = [
    # API
    path("", include(router.urls)),
    # API Authentication
    path("login/", CustomJsonWebToken.as_view()),

    path("http/", ApiFastView.as_view()),

    path("st", ProjectListViewSet.as_view())
]


# Final URL configuration
app_name = "api"
urlpatterns = app_urls + router.urls
