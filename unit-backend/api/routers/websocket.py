from django.urls import path
from api.views import consumers


socket_urlpatterns = [
    path('websocket/test', consumers.WebSocketConsumer.as_asgi()),
    # path('performance/', consumers.PerformanceConsumer.as_asgi())
]
