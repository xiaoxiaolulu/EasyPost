import re
from datetime import (
    datetime,
    timedelta
)
from typing import Any
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from api.models.user import (
    User,
    VerifyCode
)

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$" # noqa
REGEX_EMAIL = "/^[a-zA-Z0-9_\.]+@[a-zA-Z0-9-]+[\.a-zA-Z]+$/" # noqa


class UserDao:

    @staticmethod
    def validate_account_type(account: str, account_type: str) -> None:
        """验证账号类型的函数"""
        if account_type == 'mobile':
            if not re.match(REGEX_MOBILE, account):
                raise Exception("手机号码不合法! ❌")
        elif account_type == "email":
            if not re.match(REGEX_EMAIL, account):
                raise Exception("邮箱账号不合法! ❌")
        else:
            raise Exception("账号类型不合法! ❌")

    @staticmethod
    def check_user_existence(account: str) -> None:
        """检查用户是否存在的函数"""
        try:
            user = User.objects.get(mobile=account) or User.objects.get(email=account)
            if user:
                raise Exception("用户名或邮箱已存在! ❌")
        except User.DoesNotExist:
            pass

    @staticmethod
    def check_verify_code_time(account: str) -> None:
        """检查验证码发送时间的函数"""
        one_minutes_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, account=account).exists():
            raise Exception("距离上一次发送未超过60s ❌")

    def register_user_validate(self, account: str, account_type: str) -> None:
        """注册用户验证的主函数"""
        try:
            self.validate_account_type(account, account_type)
            self.check_user_existence(account)
            self.check_verify_code_time(account)
        except Exception as err:
            raise Exception(f"用户获取验证码失败 -> {err} ❌")

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
                raise Exception('验证码过期 ❌')
            if last_recode.code != code:
                raise Exception('验证码错误 ❌')
        else:
            raise Exception('账号不存在 ❌')

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
