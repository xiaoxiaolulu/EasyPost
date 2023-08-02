from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_jwt.views import (
    ObtainJSONWebToken,
    jwt_response_payload_handler
)


User = get_user_model()


class CustomAuthenticateBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
        except (User.DoesNotExist, ImproperlyConfigured):
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class CustomJsonWebToken(ObtainJSONWebToken):
    """
    重写JWT认证方法
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            print("测试")
            print(user)
            print("测试")

            token = serializer.object.get('token')
            print(token)
            print("c11111")
            response_data = jwt_response_payload_handler(token, user, request)
            response_data.update({"username": user.username, "nickname": user.nickname, "userid": user.pk})
            response = Response(response_data)
            print(response_data)
            print(2222222222222)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
