import re
from datetime import datetime, timedelta
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
