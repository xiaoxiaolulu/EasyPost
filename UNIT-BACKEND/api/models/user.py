"""
DESCRIPTION：用户模型
:Created by Null.

 * table-User: 用户
 * table-UserProfile: 用户扩展
 * table-VerifyCode: 验证码
"""
from os import path
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    Model,
    CharField,
    TextField,
    ImageField,
    DateTimeField,
    DateField,
    AutoField,
    IntegerChoices,
    TextChoices,
    BooleanField, ForeignKey, SET_NULL
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from config.settings import MEDIA_ROOT


class UserStateChoices(IntegerChoices):

    VALID = 0

    EXPIRED = 1


class UserGenderChoices(TextChoices):

    MALE = "male"

    FEMALE = "female"


class UserAccountTypeChoices(TextChoices):

    EMAIL = "email"

    MOBILE = "mobile"


class UserExtendInformation(TextChoices):

    DEPT = "Quality Testing Department"

    INTRODUCTION = "The user is lazy and didn't write anything..."


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
    id = AutoField(primary_key=True)
    nickname = CharField(max_length=20, null=True, blank=True, verbose_name=_('User Nickname'))
    mobile = CharField(max_length=11, null=True, blank=True, verbose_name=_('User Mobile'))
    email = CharField(max_length=125, null=True, blank=True, verbose_name=_('User Email'))
    introduction = TextField(blank=True, null=True, verbose_name=_('User Introduction'),
                             default=UserExtendInformation.INTRODUCTION)
    avatar = ImageField(upload_to=MEDIA_ROOT, default=path.join(MEDIA_ROOT, 'default.png'),
                        null=True, blank=True, verbose_name=_('User Avatar'))
    address = CharField(max_length=100, null=True, blank=True, verbose_name=_('User Address'))
    birthday = DateField(verbose_name=_('User Birthday'), blank=True, null=True, default=timezone.now)
    gender = CharField(verbose_name=_('User Gender'), choices=UserGenderChoices, max_length=6,
                       default=UserGenderChoices.MALE)
    dept = CharField(blank=True, null=True, verbose_name=_('User Dept'), max_length=125,
                     default=UserExtendInformation.DEPT)
    ip_address = CharField(null=True, max_length=125, verbose_name=_('User IpAddress'))
    last_login_time = DateTimeField(default=timezone.now, verbose_name=_('User LastLoginTime'))

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


class UserRole(Model):
    """
    用户权限配置
    * user: 用户
    * name: 权限名
    * key: 权限Key
    * is_super: 是否管理员
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, null=True, blank=True, verbose_name=_('UserRoleId'))
    key = CharField(max_length=100, null=True, blank=True, verbose_name=_('UserRoleId'))
    is_super = BooleanField(default=False, verbose_name=_('UserRoleIsSuper'))
    user = ForeignKey(User, null=True, on_delete=SET_NULL, related_name='roles', verbose_name=_('User'))

    class Meta:
        verbose_name = _('UserRole')
        verbose_name_plural = verbose_name
        app_label = 'api'

    def __str__(self):
        return self.name


class VerifyCode(Model):
    """
    验证码模型
    * code: 验证码
    * account: 账号
    * account: 账号类型
    * add_time: 添加时间
    """
    id = AutoField(primary_key=True)
    code = CharField(max_length=10, verbose_name=_('VerifyCode Code'))
    account = CharField(max_length=125, verbose_name=_('VerifyCode Account'))
    account_type = CharField(verbose_name=_('VerifyCode AccountType'), choices=UserAccountTypeChoices,
                             default=UserAccountTypeChoices.EMAIL, max_length=6)
    add_time = DateTimeField(default=timezone.now, verbose_name=_('VerifyCode AddTime'))

    class Meta:
        verbose_name = _("Verify Code")
        verbose_name_plural = verbose_name
        app_label = 'api'

    def __str__(self):
        return self.code
