"""
DESCRIPTION：系统配置模型
:Created by Null.

 * table-Project: 项目配置
"""
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    ForeignKey,
    SET_NULL,
    ImageField,
    AutoField
)
from django.db.models.signals import (
    post_delete,
    post_save
)
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Defaults(object):
    """
    默认字段
    * 项目类型
    """

    PROJECT_TYPE = "Web"

    PROJECT_TYPE_CHOICES = (
        ('Web', 'Web'),
        ('App', 'App'),
        ('Pc', 'Pc'),
        ('MiniProgram', 'MiniProgram')
    )

    PRIVATE_TYPE = 0

    PRIVATE_TYPE_CHOICES = (
        (0, 0),
        (1, 1)
    )


class Project(Model):
    """
    项目配置
    * name: 项目名称
    * user: 用户
    * avatar: 项目头像
    * type: 项目类型
    * desc: 描述
    * create_time: 创建时间
    * update_time: 更新时间
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Project Name'))
    user = ForeignKey(User, null=True, on_delete=SET_NULL, verbose_name=_('User'))
    type = CharField(max_length=50, verbose_name=_('Project Type'), choices=Defaults.PROJECT_TYPE_CHOICES,
                     default=Defaults.PROJECT_TYPE)
    private = CharField(max_length=50, verbose_name=_('Project private'), choices=Defaults.PRIVATE_TYPE_CHOICES,
                        default=Defaults.PRIVATE_TYPE)
    avatar = ImageField(upload_to='avatar/', default="avatar/default.png", null=True, blank=True,
                        verbose_name=_('Project Avatar'))
    desc = TextField(null=True, blank=True, verbose_name=_('Project Desc'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('Project CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('Project UpdateTime'))

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)
        app_label = 'api'

    def __str__(self):
        return self.name


class ProjectRole(Model):

    id = AutoField(primary_key=True)
    user = ForeignKey(User, null=True, on_delete=SET_NULL, verbose_name=_('User'))
    project = ForeignKey(Project, null=True, on_delete=SET_NULL, related_name='roles', verbose_name=_('Project'))
    rode_id = CharField(max_length=50, null=True, blank=True, verbose_name=_('ProjectRoleId'))


def _generate_cache_key(sender, instance):
    instance = instance
    cache_key = f"{instance.user} - {sender._meta.model_name}" # noqa

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


post_save.connect(_update_cache, sender=Project)
post_delete.connect(_delete_cache, sender=Project)
