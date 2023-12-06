"""
DESCRIPTION：用户模型
:Created by Null.

 * table-User: 用户
 * table-UserProfile: 用户扩展
 * table-VerifyCode: 验证码
"""
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    Model,
    CharField,
    TextField,
    ImageField,
    DateTimeField,
    DateField
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Defaults(object):
    """
    默认字段
    * 性别
    * 部门
    * 简介
    """

    ACCOUNT_TYPE = "email"
    DEPT = "Quality Testing Department"
    GENDER = "male"
    INTRODUCTION = "The user is lazy and didn't write anything..."

    ACCOUNT_TYPE_CHOICES = (
        ("email", "邮箱"),
        ("mobile", "手机")
    )

    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女')
    )

    IS_VALID_CHOICES = (
        (0, 0),
        (1, 1)
    )


class User(AbstractUser):
    """自定义用户模型
    * nickname: 昵称
    * mobile: 手机
    * email: 邮箱
    * introduction: 簡介
    * avatar: 头像
    * address: 用户地址
    * birthday: 生日
    * gender: 性别
    * dept: 部门
    * is_valid: 管理员可以禁用某个用户，当他离职后
    * role: 临时字段 1 管理员  2 组员  3 边缘
    """

    nickname = CharField(max_length=20, null=True, blank=True, verbose_name=_('User Nickname'))
    mobile = CharField(max_length=11, null=True, blank=True, verbose_name=_('User Mobile'))
    email = CharField(max_length=125, null=True, blank=True, verbose_name=_('User Email'))
    introduction = TextField(blank=True, null=True, verbose_name=_('User Introduction'), default=Defaults.INTRODUCTION)
    avatar = ImageField(upload_to='avatar/', default="avatar/default.png", null=True, blank=True, verbose_name=_('User Avatar'))
    address = CharField(max_length=100, null=True, blank=True, verbose_name=_('User Address'))
    birthday = DateField(verbose_name=_('User Birthday'), blank=True, null=True, default=timezone.now)
    gender = CharField(verbose_name=_('User Gender'), choices=Defaults.GENDER_CHOICES, max_length=6,
                       default=Defaults.GENDER)
    dept = CharField(blank=True, null=True, verbose_name=_('User Dept'), max_length=125, default=Defaults.DEPT)
    # 临时
    role = CharField(max_length=20, null=True, blank=True, verbose_name=_('User Role'))

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = verbose_name
        app_label = 'api'

    def __str__(self):
        return self.username

    def get_profile_name(self):
        if self.nickname:
            return self.nickname
        return self.username


class VerifyCode(Model):
    """
    验证码模型
    * code: 验证码
    * account: 账号
    * account: 账号类型
    * add_time: 添加时间
    """

    code = CharField(max_length=10, verbose_name=_('VerifyCode Code'))
    account = CharField(max_length=125, verbose_name=_('VerifyCode Account'))
    account_type = CharField(verbose_name=_('VerifyCode AccountType'), choices=Defaults.ACCOUNT_TYPE_CHOICES,
                             default=Defaults.ACCOUNT_TYPE, max_length=6)
    add_time = DateTimeField(default=timezone.now, verbose_name=_('VerifyCode AddTime'))

    class Meta:
        verbose_name = _("Verify Code")
        verbose_name_plural = verbose_name
        app_label = 'api'

    def __str__(self):
        return self.code
