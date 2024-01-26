from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    SET_NULL,
    TextField,
    AutoField
)
from django.db.models.signals import (
    post_save,
    post_delete
)
from django.utils.translation import gettext_lazy as _

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
    id = AutoField(primary_key=True)
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
    id = AutoField(primary_key=True)
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


def _generate_cache_key(sender, instance):  # noqa
    instance = instance
    cache_key = f"{instance.user} - {sender._meta.model_name}"  # noqa

    return cache_key


def _update_cache(sender, **kwargs):
    instance = kwargs.get('instance')
    cache_key = _generate_cache_key(sender, instance)

    cache_response = cache.get(cache_key)
    if cache_response:
        cache.delete(cache_key)


def _delete_cache(sender, **kwargs):
    instance = kwargs.get('instance')
    cache_key = _generate_cache_key(sender, instance)
    cache.delete(cache_key)


post_save.connect(_update_cache, sender=TestEnvironment)
post_delete.connect(_delete_cache, sender=TestEnvironment)
post_save.connect(_update_cache, sender=Address)
post_delete.connect(_delete_cache, sender=Address)
