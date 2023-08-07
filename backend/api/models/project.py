"""
DESCRIPTION：系统配置模型
:Created by Null.

 * table-Project: 项目配置
"""
from django.contrib.auth import get_user_model
from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    ForeignKey,
    SET_NULL,
    ImageField,
    IntegerField
)
from django.utils.translation import ugettext_lazy as _

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
