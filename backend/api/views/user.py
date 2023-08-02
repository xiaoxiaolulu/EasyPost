from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.views import (
    ObtainJSONWebToken,
    jwt_response_payload_handler
)

from utils.fatcory import ResponseStandard

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

            token = serializer.object.get('token')
            jwt_response_payload_handler(token, user, request)

            response = ResponseStandard.model_to_dict(user, exclude="password")
            response = Response(ResponseStandard.success(dict(token=token, userInfo=response, roles=[user.role])))

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
