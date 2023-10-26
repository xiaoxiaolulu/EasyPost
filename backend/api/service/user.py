from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_response_payload_handler
from rest_framework_jwt.views import ObtainJSONWebToken
from api.response.magic import MagicListAPI
from api.schema.user import UserSimpleSerializers
from core.exception.exception_handler import jwt_response_payload_error_handler
from api.response.fatcory import ResponseStandard

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

            token = jwt_response_payload_handler(token, user, request)
            response = {"username": user.username, "nickname": user.nickname, "userid": user.pk}
            response = Response(ResponseStandard.success(dict(token, userInfo=response, roles=[user.role])))

            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response


class UserListViewSet(MagicListAPI):

    queryset = User.objects.all()
    serializer_class = UserSimpleSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    ordering_fields = ['create_time']

