from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView
from api.response.magic import MagicListAPI
from api.schema.user import UserSimpleSerializers
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


class NewTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user_info = {"username": self.user.username, "nickname": self.user.nickname, "userid": self.user.pk}

        refresh = self.get_token(self.user)

        data['token'] = str(refresh.access_token)
        data['userInfo'] = user_info
        data['roles'] = [self.user.role]

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        response = ResponseStandard.success(data)
        return response


class CustomJsonWebToken(TokenObtainPairView):
    """
    重写JWT认证方法
    """
    serializer_class = NewTokenObtainPairSerializer


class UserListViewSet(MagicListAPI):

    queryset = User.objects.all()
    serializer_class = UserSimpleSerializers
    permission_classes = [IsAuthenticated]
    ordering_fields = ['create_time']
