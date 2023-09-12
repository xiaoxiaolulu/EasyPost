from django.contrib.auth import get_user_model
from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    SET_NULL,
    TextField
)
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class TestEnvironment(Model):
    """
    项目环境配置
    * name: 环境名称
    * user: 用户
    * desc: 描述
    * create_time: 创建时间
    * update_time: 更新时间
    """

    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('TestEnvironment Name'))
    user = ForeignKey(User, null=True, on_delete=SET_NULL, verbose_name=_('User'))
    desc = TextField(null=True, blank=True, verbose_name=_('TestEnvironment Desc'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('TestEnvironment CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('TestEnvironment UpdateTime'))

    class Meta:
        verbose_name = _("Test Environment")
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)

    def __str__(self):
        return self.name


class Address(Model):
    """
    项目地址配置
    * env: 所属环境
    * name: 环境名称
    * host: 地址
    * user: 用户
    * create_time: 创建时间
    * update_time: 更新时间
    """

    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Address Name'))
    env = ForeignKey(TestEnvironment, null=True, on_delete=SET_NULL, verbose_name=_('Address Env'))
    host = CharField(max_length=100, null=True, blank=True, verbose_name=_('Address Host'))
    user = ForeignKey(User, related_name="address_creator", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('Address CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('Address UpdateTime'))

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)

    def __str__(self):
        return self.name
