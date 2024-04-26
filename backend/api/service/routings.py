from django.urls import path
# 当前文件同级目录下创建consumers.py文件
from . import consumers

# 这个变量是存放websocket的路由
socket_urlpatterns = [
    path('websocket/test', consumers.WebSocketForwardConsumer.as_asgi()),
]
