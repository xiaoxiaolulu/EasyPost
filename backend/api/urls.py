from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.https import ApiFastView
from api.views.user import CustomJsonWebToken

router = DefaultRouter()

app_urls = [
    # API
    path("", include(router.urls)),
    # API Authentication
    path("login/", CustomJsonWebToken.as_view()),

    path("http/", ApiFastView.as_view())
]


# Final URL configuration
app_name = "api"
urlpatterns = app_urls + router.urls
