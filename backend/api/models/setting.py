"""
DESCRIPTION：设置模型
:Created by Null.

 * table-TestEnvironment: 环境配置
 * table-DataSource: 数据库配置
 * table-BindDataSource: 关联的数据库
"""
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
    * server: 环境配置
    * variables: 变量池
    * user: 用户
    * desc: 描述
    * create_time: 创建时间
    * update_time: 更新时间
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('TestEnvironment Name'))
    server = TextField(null=True, blank=True, verbose_name=_('TestEnvironment Server'))
    variables = TextField(null=True, blank=True, verbose_name=_('TestEnvironment Variables'))
    user = ForeignKey(User, null=True, on_delete=SET_NULL, verbose_name=_('User'))
    remarks = TextField(null=True, blank=True, verbose_name=_('TestEnvironment Desc'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('TestEnvironment CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('TestEnvironment UpdateTime'))

    class Meta:
        verbose_name = _("Test Environment")
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)

    def __str__(self):
        return self.name


class DataSource(Model):
    """
    数据库配置
    * name: 数据库名称
    * host: 地址
    * port: 端口
    * user: 账号
    * password: 密码
    * creator: 用户
    * create_time: 创建时间
    * update_time: 更新时间
    """
    id = AutoField(primary_key=True)
    database = CharField(max_length=50, null=True, blank=True, verbose_name=_('DataSource Name'))
    host = CharField(max_length=100, null=True, blank=True, verbose_name=_('DataSource Host'))
    port = CharField(max_length=100, null=True, blank=True, verbose_name=_('DataSource Port'))
    user = CharField(max_length=100, null=True, blank=True, verbose_name=_('DataSource User'))
    password = CharField(max_length=100, null=True, blank=True, verbose_name=_('DataSource Host'))
    creator = ForeignKey(User, related_name="data_source", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('DataSource CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('DataSource UpdateTime'))

    class Meta:
        verbose_name = _("DataSource")
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)

    def __str__(self):
        return self.database


class BindDataSource(Model):
    """
    数据库配置
    * name: 数据库名称
    * env: 所属环境
    * host: 地址
    * port: 端口
    * user: 账号
    * password: 密码
    * creator: 用户
    * create_time: 创建时间
    * update_time: 更新时间
    """
    id = AutoField(primary_key=True)
    env = ForeignKey(
        TestEnvironment, null=True, on_delete=SET_NULL, related_name='data_source', verbose_name=_('BindDataSource env'))
    database = CharField(max_length=50, null=True, blank=True, verbose_name=_('BindDataSource Name'))
    host = CharField(max_length=100, null=True, blank=True, verbose_name=_('BindDataSource Host'))
    port = CharField(max_length=100, null=True, blank=True, verbose_name=_('BindDataSource Port'))
    user = CharField(max_length=100, null=True, blank=True, verbose_name=_('BindDataSource User'))
    password = CharField(max_length=100, null=True, blank=True, verbose_name=_('BindDataSource Host'))
    creator = ForeignKey(User, related_name="bind_source", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('BindDataSource CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('BindDataSource UpdateTime'))

    class Meta:
        verbose_name = _("DataSource")
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)

    def __str__(self):
        return self.database


class Functions(Model):
    """
    内置函数
    * name: 内置函数名称
    * content: 内置函数内容
    * remarks: 内置函数描述
    * creator: 用户
    * create_time: 创建时间
    * update_time: 更新时间
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Functions Name'))
    content = TextField(null=True, blank=True, verbose_name=_('Functions Content'))
    remarks = TextField(null=True, blank=True, verbose_name=_('Functions Remarks'))
    creator = ForeignKey(User, related_name="functions_creator", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('Functions CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('Functions UpdateTime'))

    class Meta:
        verbose_name = _("Functions")
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
