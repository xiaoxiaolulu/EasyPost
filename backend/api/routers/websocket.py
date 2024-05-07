from django.urls import path
from api.service import consumers


socket_urlpatterns = [
    path('websocket/test', consumers.WebSocketConsumer.as_asgi()),
]
