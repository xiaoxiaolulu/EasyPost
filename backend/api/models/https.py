"""
DESCRIPTION：接口测试模型
:Created by Null.

 * table-Relation: 目录结构
 * table-Api: 接口文档
 * table-Case: 接口用例
 * table-Step: 接口步骤
 * table-ApiCopy: 接口快照
 * table-DataStructure: 数据结构
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
    ManyToManyField, IntegerChoices
)
from api.models.project import Project
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Defaults(object):
    """
    默认字段
    * 状态
    * 优先级
    * 目录类型
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

    TREE_TYPE = 0

    TREE_TYPE_CHOICES = (
        (0, 0),
        (1, 1)
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
    type = CharField(max_length=50, verbose_name=_('Relation Type'), default=Defaults.TREE_TYPE,
                     choices=Defaults.TREE_TYPE_CHOICES)

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
    * method: 请求类型
    * url: 路由
    * headers: 请求头
    * body: 请求体
    * directory_id: 目录id
    * project:关联项目
    * desc: 描述
    * params: 地址参数
    * raw: 请求体
    * setup_script: 前置步骤
    * teardown_script: 后置步骤
    * validate: 校验内容
    * extract: 提取参数
    * user: 创建者
    * create_time: 创建时间
    * update_time: 更新时间
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=250, null=True, blank=True, verbose_name=_('Api Name'))
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
    source = TextField(verbose_name=_('Api Source'), null=False, default=None)
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('Api CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('Api UpdateTime'))

    class Meta:
        verbose_name = _('Api')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Case(Model):
    """
    用例

    * name: 接口名称
    * priority: 优先级 P0/P1/P2/P3
    * project: 关联项目
    * directory_id: 目录id
    * rerun: 重试次数
    * threads: 线程数
    * desc: 描述
    * user: 创建者
    * create_time: 创建时间
    * update_time: 更新时间
    """
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
    """
    步骤

    * sort: 序号
    * case: 关联用例
    * name: 步骤名称
    * method: 请求类型
    * url: 路由
    * headers: 请求头
    * params: 地址参数
    * raw: 请求体
    * setup_script: 前置脚本
    * teardown_script: 后置脚本
    * validate: 校验内容
    * extract: 提取参数
    * desc: 描述
    * user: 创建者
    * create_time: 创建时间
    * update_time: 更新时间
    """
    id = AutoField(primary_key=True)
    sort = CharField(max_length=50, null=True, blank=True, verbose_name=_('Step Sort'))
    case = ForeignKey(Case, null=True, on_delete=SET_NULL, related_name='step', verbose_name=_('Step Case'))
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
    user = ForeignKey(User, related_name="step_creator", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('Step CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('Step UpdateTime'))

    class Meta:
        verbose_name = _('Step')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DataStructureType(IntegerChoices):

    NONE = 0
    FORM_DATA = 1
    X_WWW_FORM_URLENCODED = 2
    RAW = 3


class DataStructure(Model):

    """
    数据结构

    * name: 数据结构名称
    * desc: 描述
    * raw: 参数
    * user: 创建者
    * create_time: 创建时间
    * update_time: 更新时间
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('DataStructure Name'))
    desc = TextField(null=True, blank=True, verbose_name=_('DataStructure Desc'))
    type = CharField(max_length=50, verbose_name=_('DataStructure Type'), choices=DataStructureType,
                     default=DataStructureType.NONE)
    raw = TextField(verbose_name=_('DataStructure raw'), null=False,  default=None)
    user = ForeignKey(User, related_name="datastructure_creator", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('DataStructure CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('DataStructure UpdateTime'))

    class Meta:
        verbose_name = _('ApiCopy')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ApiCopy(Model):

    """
    接口快照

    * name: 接口名称
    * priority: 优先级 P0/P1/P2/P3
    * status: 接口状态 调试中 0 已废弃 1 正常 2
    * request_type： 请求类型  http 1 grpc 2 dubbo 3
    * method: 请求类型
    * url: 路由
    * headers: 请求头
    * body: 请求体
    * directory_id: 目录id
    * project:关联项目
    * desc: 描述
    * params: 地址参数
    * raw: 请求体
    * setup_script: 前置步骤
    * teardown_script: 后置步骤
    * validate: 校验内容
    * extract: 提取参数
    * user: 创建者
    * create_time: 创建时间
    * update_time: 更新时间
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('ApiCopy Name'))
    project = ForeignKey(Project, on_delete=CASCADE, db_constraint=False)
    directory_id = CharField(max_length=50, null=True, blank=True, verbose_name=_('ApiCopy DirectoryId'))
    method = CharField(max_length=50, null=True, blank=True, verbose_name=_('ApiCopy Method'))
    url = TextField(verbose_name=_('Api Url'), null=False, default=None)
    priority = CharField(max_length=50, verbose_name=_('ApiCopy Priority'), choices=Defaults.PRIORITY_TYPE_CHOICES,
                         default=Defaults.PRIORITY_TYPE)
    status = CharField(max_length=50, verbose_name=_('ApiCopy Status'), choices=Defaults.STATUS_CHOICES,
                       default=Defaults.STATUS_TYPE)
    desc = TextField(null=True, blank=True, verbose_name=_('ApiCopy Desc'))
    headers = TextField(verbose_name=_('ApiCopy Headers'), null=False, default=None)
    params = TextField(verbose_name=_('ApiCopy Params'), null=False, default=None)
    raw = TextField(verbose_name=_('ApiCopy raw'), null=False,  default=None)
    setup_script = TextField(verbose_name=_('ApiCopy SetupScript'), null=False,  default=None)
    teardown_script = TextField(verbose_name=_('ApiCopy TeardownScript'), null=False, default=None)
    validate = TextField(verbose_name=_('ApiCopy Validate'), null=False, default=None)
    extract = TextField(verbose_name=_('ApiCopy Extract'), null=False, default=None)
    user = ForeignKey(User, related_name="apiCopy_creator", null=True, on_delete=SET_NULL, verbose_name=_('User'))
    create_time = DateTimeField(auto_now_add=True, verbose_name=_('ApiCopy CreateTime'))
    update_time = DateTimeField(auto_now=True, verbose_name=_('ApiCopy UpdateTime'))

    class Meta:
        verbose_name = _('ApiCopy')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
