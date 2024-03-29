"""
DESCRIPTION：计划模型
:Created by Null.

 * table-Plan: 测试计划
"""
from django.contrib.auth import get_user_model
from django.db.models import (
    Model,
    ForeignKey,
    CASCADE,
    TextField,
    CharField,
    DateTimeField,
    SET_NULL,
    AutoField,
    ManyToManyField
)
from api.models.project import Project
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Defaults(object):
    """
    默认字段
    * 优先级
    * 状态
    """

    PRIORITY_TYPE = 0

    PRIORITY_TYPE_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    )

    STATE_TYPE = 0

    STATE_CHOICES = (
        (0, 0),
        (1, 1)
    )


class Plan(Model):
    """
    测试计划
    * name: 项目名称
    * project: 关联项目
    * cron: cron表达式
    * priority: 优先级
    * case_list: 关联用例列表
    * state: 状态
    * user: 用户
    * pass_rate: 通过率
    * msg_type: 通过类型
    * receiver: 收件人
    * create_time: 创建时间
    * update_time: 更新时间
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Plan Name'))
    project = ForeignKey(Project, on_delete=CASCADE, db_constraint=False)
    cron = TextField(verbose_name=_('Plan Cron'), null=False, default=None)
    priority = CharField(max_length=50, verbose_name=_('Plan Priority'), choices=Defaults.PRIORITY_TYPE_CHOICES,
                         default=Defaults.PRIORITY_TYPE)
    case_list = TextField(verbose_name=_('Plan CaseList'), null=False, default=None)
    state = CharField(max_length=50, verbose_name=_('Plan State'), choices=Defaults.STATE_CHOICES,
                      default=Defaults.STATE_TYPE)
    pass_rate = CharField(max_length=50, null=True, blank=True, verbose_name=_('Plan PassRate'))
    msg_type = CharField(max_length=50, null=True, blank=True, verbose_name=_('Plan MsgType'))
    receiver = TextField(verbose_name=_('Plan Receiver'), null=False, default=None)
    user = ForeignKey(User, related_name="plan_creator", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('Plan CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('Plan UpdateTime'))

    class Meta:
        verbose_name = _('Plan')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
