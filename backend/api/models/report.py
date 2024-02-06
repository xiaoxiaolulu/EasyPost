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
    id = AutoField(primary_key=True)
    detail = ForeignKey(Detail, null=True, on_delete=SET_NULL, related_name='detail_step',
                        verbose_name=_('DetailStep Step'))
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
