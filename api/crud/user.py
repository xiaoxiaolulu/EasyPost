import re
from datetime import datetime, timedelta
from typing import Any
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.db.models.functions import Log
from api.models.user import User, VerifyCode

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$" # noqa
REGEX_EMAIL = "/^[a-zA-Z0-9_\.]+@[a-zA-Z0-9-]+[\.a-zA-Z]+$/" # noqa


class UserDao:

    log = Log("UserDao")

    @staticmethod
    def register_user_validate(account: str, account_type: str) -> None:
        """
        注册用户验证
        :param account:  注册账号, str object.
        :param account_type: 账号类型, str object.
        :return: None
        """
        try:
            user = User.objects.filter(Q(mobile=account) | Q(email=account)).first()

            if user:
                raise Exception("用户名或邮箱已存在!")

            if account_type == 'mobile':
                if not re.match(REGEX_MOBILE, account):
                    raise Exception("手机号码不合法!")

            if account_type == "email":
                if not re.match(REGEX_EMAIL, account):
                    raise Exception("邮箱账号不合法!")

            one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
            if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, account=account).count():
                raise Exception("距离上一次发送未超过60s")

        except Exception as err:
            UserDao.log.error(f"用户获取验证码失败 -> {str(err)}")
            raise Exception(f"用户获取验证码失败 -> {err}")

    @staticmethod
    def register_code_validate(account: str, account_type: str, code: str) -> None:
        """
        注册验证码验证
        :param account: 账号, str object.
        :param account_type: 账号类型, str object.
        :param code: 验证码, str object.
        :return: None
        """

        existed = VerifyCode.objects.filter(account_type=account_type, account=account).order_by('-add_time')
        if existed:
            last_recode = existed[0]
            one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)

            if one_minutes_ago > last_recode.add_time:
                UserDao.log.error("验证码已过期!")
                raise Exception('验证码过期')
            if last_recode.code != code:
                UserDao.log.error(f"验证码错误 -> {code}")
                raise Exception('验证码错误')
        else:
            UserDao.log.error(f"账号不存在 -> {account}")
            raise Exception('账号不存在')

    @staticmethod
    def get_username(username: str) -> Any | None:
        """
        校验用户是否注册
        :param username: 用户名
        :return: User.objects
        """

        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
            return user
        except (User.DoesNotExist, ImproperlyConfigured):
            return None

    @staticmethod
    def get_register_code(account: str, account_type: str, code: str) -> None:
        """
        获取注册验证码
        :param account: 账号, str object.
        :param account_type: 账号类型, str object.
        :param code: 验证码, str object.
        :return: None
        """

        verify_code = VerifyCode(code=code, account=account, account_type=account_type)
        verify_code.save()

    @staticmethod
    def query_user_by_email(email: str) -> Any | None:
        """
        根据邮箱获取用户
        :param email: 注册邮箱, str object.
        :return: User.objects
        """

        try:
            user = User.objects.get(email=email).first()
            return user
        except (User.DoesNotExist, ImproperlyConfigured):
            return None

    @staticmethod
    def rest_password(username: str, password: str) -> None:
        """
        重置验证码
        :param username: 账号, str object.
        :param password: 密码, str object.
        :return: None
        """

        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))

            if user:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()

        except (User.DoesNotExist, ImproperlyConfigured):
            return None
