"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from api.routers.websocket import socket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    # 当存在http请求时，路由走这里
    "http": get_asgi_application(),
    # 当存在websocket请求时，将请求交给指定应用中的路由模块处理
    "websocket": URLRouter(socket_urlpatterns)
})
