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
    """
    STATUS_TYPE = 0

    STATUS_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2)
    )

    PRIORITY_TYPE = 0

    PRIORITY_TYPE_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    )


class Relation(Model):
    """
    树形结构关系

    * project: 关联项目
    * tree: 树形名称
    * type: 树形类型
    """
    id = AutoField(primary_key=True)
    project = ForeignKey(Project, on_delete=CASCADE, db_constraint=False)
    tree = TextField(verbose_name=_('Relation Tree'), null=False, default=[])

    class Meta:
        verbose_name = _('Relation')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tree


class Api(Model):
    """
    接口

    * name: 接口名称
    * priority: 优先级 P0/P1/P2/P3
    * status: 接口状态 调试中 0 已废弃 1 正常 2
    * request_type： 请求类型  http 1 grpc 2 dubbo 3
    * tag: 标签
    * gateway: 前置url
    * request_method: 请求类型
    * url: 路由
    * request_headers: 请求头
    * body: 请求体
    * directory_id: 目录id
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Api Name'))
    project = ForeignKey(Project, on_delete=CASCADE, db_constraint=False)
    directory_id = CharField(max_length=50, null=True, blank=True, verbose_name=_('Api DirectoryId'))
    method = CharField(max_length=50, null=True, blank=True, verbose_name=_('Api Method'))
    url = TextField(verbose_name=_('Api Url'), null=False, default=None)
    priority = CharField(max_length=50, verbose_name=_('Api Priority'), choices=Defaults.PRIORITY_TYPE_CHOICES,
                       default=Defaults.PRIORITY_TYPE)
    status = CharField(max_length=50, verbose_name=_('Api Status'), choices=Defaults.STATUS_CHOICES,
                       default=Defaults.STATUS_TYPE)
    desc = TextField(null=True, blank=True, verbose_name=_('Api Desc'))
    headers = TextField(verbose_name=_('Api Headers'), null=False, default=None)
    params = TextField(verbose_name=_('Api Params'), null=False, default=None)
    raw = TextField(verbose_name=_('Api raw'), null=False,  default=None)
    setup_script = TextField(verbose_name=_('Api SetupScript'), null=False,  default=None)
    teardown_script = TextField(verbose_name=_('Api TeardownScript'), null=False, default=None)
    validate = TextField(verbose_name=_('Api Validate'), null=False, default=None)
    extract = TextField(verbose_name=_('Api Extract'), null=False, default=None)
    user = ForeignKey(User, related_name="api_creator", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('Api CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('Api UpdateTime'))

    class Meta:
        verbose_name = _('Api')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Case(Model):

    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Case Name'))
    project = ForeignKey(Project, on_delete=CASCADE, db_constraint=False)
    directory_id = CharField(max_length=50, null=True, blank=True, verbose_name=_('Case DirectoryId'))
    priority = CharField(max_length=50, verbose_name=_('Case Priority'), choices=Defaults.PRIORITY_TYPE_CHOICES,
                         default=Defaults.PRIORITY_TYPE)
    rerun = CharField(max_length=50, null=True, blank=True, verbose_name=_('Case Name'))
    threads = CharField(max_length=50, null=True, blank=True, verbose_name=_('Case Name'))
    desc = TextField(null=True, blank=True, verbose_name=_('Case Desc'))
    user = ForeignKey(User, related_name="case_creator", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('Case CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('Case UpdateTime'))

    class Meta:
        verbose_name = _('Case')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Step(Model):

    id = AutoField(primary_key=True)
    sort = CharField(max_length=50, null=True, blank=True, verbose_name=_('Step Sort'))
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Step Name'))
    method = CharField(max_length=50, null=True, blank=True, verbose_name=_('Step Method'))
    url = TextField(verbose_name=_('Step Url'), null=False, default=None)
    desc = TextField(null=True, blank=True, verbose_name=_('Step Desc'))
    headers = TextField(verbose_name=_('Step Headers'), null=False, default=None)
    params = TextField(verbose_name=_('Step Params'), null=False, default=None)
    raw = TextField(verbose_name=_('Step raw'), null=False,  default=None)
    setup_script = TextField(verbose_name=_('Step SetupScript'), null=False,  default=None)
    teardown_script = TextField(verbose_name=_('Step TeardownScript'), null=False, default=None)
    validate = TextField(verbose_name=_('Step Validate'), null=False, default=None)
    extract = TextField(verbose_name=_('Step Extract'), null=False, default=None)
    case = ForeignKey(Case, null=True, on_delete=SET_NULL, related_name='step', verbose_name=_('Case'))
    user = ForeignKey(User, related_name="step_creator", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('Step CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('Step UpdateTime'))

    class Meta:
        verbose_name = _('Step')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
