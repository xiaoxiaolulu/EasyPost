"""
DESCRIPTION：报告模型
:Created by Null.

 * table-Main: 报告主内容
 * table-Detail: 报告详情
  * table-DetailStep: 报告详情步骤
"""
from django.contrib.auth import get_user_model
from django.db.models import (
    Model,
    ForeignKey,
    TextField,
    CharField,
    SET_NULL,
    AutoField
)
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Main(Model):
    """
    测试报告
    * name: 报告名称
    * state: 报告状态
    * all: 用例总数
    * success: 用例成功数
    * error: 用例错误数
    * fail: 用例失败数
    * runtime: 运行时间
    * begin_time: 开始执行时间
    * argtime: 平均运行时间
    * pass_rate: 通过率
    * tester: 测试人员
    """

    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main Name'))
    state = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main State'))
    all = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main All'))
    success = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main Success'))
    error = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main Error'))
    fail = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main Fail'))
    runtime = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main Runtime'))
    begin_time = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main BeginTime'))
    argtime = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main Argtime'))
    pass_rate = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main PassRate'))
    tester = CharField(max_length=50, null=True, blank=True, verbose_name=_('Main Tester'))

    class Meta:
        verbose_name = _('Main')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Detail(Model):
    """
    测试报告详情
    * report: 关联主报告
    * name: 报告名称
    * state: 报告状态
    * all: 用例总数
    * success: 用例成功数
    * error: 用例错误数
    * fail: 用例失败数
    """
    id = AutoField(primary_key=True)
    report = ForeignKey(Main, null=True, on_delete=SET_NULL, related_name='report_detail',
                        verbose_name=_('Detail Response'))
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Detail Name'))
    state = CharField(max_length=50, null=True, blank=True, verbose_name=_('Detail State'))
    all = CharField(max_length=50, null=True, blank=True, verbose_name=_('Detail All'))
    success = CharField(max_length=50, null=True, blank=True, verbose_name=_('Detail Success'))
    error = CharField(max_length=50, null=True, blank=True, verbose_name=_('Detail Error'))
    fail = CharField(max_length=50, null=True, blank=True, verbose_name=_('Detail Fail'))

    class Meta:
        verbose_name = _('Detail')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DetailStep(Model):
    """
    测试报告详情步骤
    * detail: 关联报告详情
    * name: 报告名称
    * log_data: 日志
    * url: 请求地址
    * method: 请求方法
    * status_code: 状态码
    * response_header: 响应头
    * requests_header: 请求头
    * response_body: 响应体
    * requests_body: 请求体
    * state: 状态
    * run_time: 运行时间
    * validate_extractor: 验证内容
    * extras: 提取参数
    """
    id = AutoField(primary_key=True)
    sort = CharField(max_length=200, null=True, blank=True, verbose_name=_('DetailStep sort'))
    detail = ForeignKey(Detail, null=True, on_delete=SET_NULL, related_name='steps', verbose_name=_('DetailStep Step'))
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('DetailStep Name'))
    log_data = TextField(verbose_name=_('DetailStep LogData'), null=False, default=None)
    url = CharField(max_length=50, null=True, blank=True, verbose_name=_('DetailStep Url'))
    method = CharField(max_length=50, null=True, blank=True, verbose_name=_('DetailStep Method'))
    status_code = CharField(max_length=50, null=True, blank=True, verbose_name=_('DetailStep StatusCode'))
    response_header = TextField(verbose_name=_('DetailStep ResponseHeader'), null=False, default=None)
    requests_header = TextField(verbose_name=_('DetailStep RequestHeader'), null=False, default=None)
    response_body = TextField(verbose_name=_('DetailStep ResponseBody'), null=False, default=None)
    requests_body = TextField(verbose_name=_('DetailStep RequestBody'), null=False, default=None)
    state = CharField(max_length=50, null=True, blank=True, verbose_name=_('DetailStep State'))
    run_time = CharField(max_length=50, null=True, blank=True, verbose_name=_('DetailStep RunTime'))
    validate_extractor = TextField(verbose_name=_('DetailStep ValidateExtractor'), null=False, default=None)
    extras = TextField(verbose_name=_('DetailStep Extras'), null=False, default=None)

    class Meta:
        verbose_name = _('DetailStep')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
