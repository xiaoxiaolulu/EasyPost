from django.db.models import (
    Model,
    ForeignKey,
    CASCADE,
    TextField
)
from api.models.project import Project
from django.utils.translation import ugettext_lazy as _


class Relation(Model):
    """
    树形结构关系

    * project: 关联项目
    * tree: 树形名称
    * type: 树形类型
    """

    project = ForeignKey(Project, on_delete=CASCADE, db_constraint=False)
    tree = TextField(verbose_name=_('Relation Tree'), null=False, default=[])

    class Meta:
        verbose_name = _('Relation')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tree
