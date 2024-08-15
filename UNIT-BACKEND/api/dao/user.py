"""
DESCRIPTION：用户数据访问对象
:Created by Null.
"""
import re
import socket
from datetime import (
    datetime,
    timedelta
)
from typing import (
    Any
)
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
        """
        Validates an account based on its type (mobile or email) using regular expressions.

        Args:
            account: The account string to be validated.
            account_type: The type of account to validate (mobile or email).

        Raises:
            Exception: If the account type is invalid or the account does not match the
            corresponding regular expression.
        """
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
        """
        Checks if a user with the given account (mobile or email) already exists in the database.

        Args:
            account: The account string to be checked.

        Raises:
            Exception: If a user with the provided account already exists.
        """
        try:
            user = User.objects.get(mobile=account) or User.objects.get(email=account)
            if user:
                raise Exception("用户名或邮箱已存在! ❌")
        except User.DoesNotExist:
            pass

    @staticmethod
    def check_verify_code_time(account: str) -> None:
        """
        Checks if the last verification code sent to the given account was sent less than a minute ago.

        Args:
            account: The account string to be checked.

        Raises:
            Exception: If the last verification code was sent less than a minute ago.
        """
        one_minutes_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, account=account).exists():
            raise Exception("距离上一次发送未超过60s ❌")

    def register_user_validate(self, account: str, account_type: str) -> None:
        """
        Validates the account and verification code for user registration.

        Args:
            account: The account string (mobile or email) to be validated.
            account_type: The type of account to validate (mobile or email).

        Raises:
            Exception: If any of the validation steps fail.
        """
        try:
            self.validate_account_type(account, account_type)
            self.check_user_existence(account)
            self.check_verify_code_time(account)
        except Exception as err:
            raise Exception(f"用户获取验证码失败 -> {err} ❌")

    @staticmethod
    def register_code_validate(account: str, account_type: str, code: str) -> None:
        """
        Validates the verification code for user registration.

        Args:
            account: The account string (mobile or email) used for verification.
            account_type: The type of account (mobile or email).
            code: The verification code entered by the user.

        Raises:
            Exception: If the verification code is invalid or the account doesn't exist.
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
        Retrieves a user object based on the provided username.

        Args:
            username: The username string to search for. This can be the actual username,
                     mobile number, or email address associated with the user.

        Returns:
            A User object if a matching user is found, otherwise None.

        Raises:
            (User.DoesNotExist, ImproperlyConfigured): These exceptions are caught
                and not re-raised, but their occurrence is simply indicated by returning None.
        """
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
            return user
        except (User.DoesNotExist, ImproperlyConfigured):
            return None

    @staticmethod
    def get_register_code(account: str, account_type: str, code: str) -> None:
        """
        Saves a verification code for a user account.

        Args:
            account: The account string (mobile or email) associated with the code.
            account_type: The type of account (mobile or email).
            code: The verification code itself.
        """
        verify_code = VerifyCode(code=code, account=account, account_type=account_type)
        verify_code.save()

    @staticmethod
    def query_user_by_email(email: str) -> Any | None:
        """
        Retrieves a user object based on the provided email address.

        Args:
            email: The email string to search for.

        Returns:
            A User object if a matching user is found, otherwise None.

        Raises:
            (User.DoesNotExist, ImproperlyConfigured): These exceptions are caught
                and not re-raised, but their occurrence is simply indicated by returning None.
        """
        try:
            user = User.objects.get(email=email).first()
            return user
        except (User.DoesNotExist, ImproperlyConfigured):
            return None

    @staticmethod
    def rest_password(username: str, password: str) -> None:
        """
        Resets the password for a user based on username (or mobile/email).

        Args:
            username: The username (or mobile number or email address) associated with the account.
            password: The new password to set for the user.

        Raises:
            (User.DoesNotExist, ImproperlyConfigured): These exceptions are caught
                and not re-raised, but their occurrence is simply indicated by returning None.
        """
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))

            if user:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()

        except (User.DoesNotExist, ImproperlyConfigured):
            return None

    @staticmethod
    def update_user_ip(pk: int) -> None:
        """Updates the IP address of a user based on the current host's IP.

        Args:
            pk: The primary key of the user to update.

        Returns:
            None
        """
        try:
            user = User.objects.get(pk=pk)
            user.ip_address = str(socket.gethostbyname(socket.gethostname()))
            user.save()
        except (User.DoesNotExist, ImproperlyConfigured):
            pass
