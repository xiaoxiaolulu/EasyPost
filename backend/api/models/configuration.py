from django.core.cache import cache
from django.db.models import (
    Model,
    AutoField,
    CharField
)
from django.db.models.signals import (
    pre_save,
    post_delete
)
from django.utils.translation import gettext_lazy as _


ADMIN_ACCESS_WHITELIST_PREFIX = 'DJANGO_ADMIN_ACCESS_WHITELIST:'
WHITELIST_PREFIX = 'DJANGO_ADMIN_ACCESS_WHITELIST:'


class DjangoAdminAccessIPWhitelist(Model):
    """
    系统白名单
    """
    id = AutoField(primary_key=True)
    whitelist_reason = CharField(max_length=255, null=True, blank=True, help_text="Reason for the whitelist?")
    name = CharField(max_length=255, null=True, blank=True, help_text="Enter username to whitelist")

    def __unicode__(self):
        return "Whitelisted %s (%s)" % (self.name, self.whitelist_reason)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    class Meta:
        permissions = (("can_whitelist_user", "Can Whitelist User"),)
        verbose_name = _('DjangoAdminAccessIPWhitelist')
        verbose_name_plural = verbose_name
        db_table = 'django_admin_access_ip_whitelist'


def _generate_cache_key(instance):
    return ADMIN_ACCESS_WHITELIST_PREFIX + instance.name


def _update_cache(sender, **kwargs):

    new_instance = kwargs.get('instance')

    if new_instance.pk:
        old_instance = DjangoAdminAccessIPWhitelist.objects.get(
            pk=new_instance.pk)

        if _generate_cache_key(old_instance) != \
            _generate_cache_key(new_instance):
            old_cache_key = _generate_cache_key(old_instance)
            cache.delete(old_cache_key)

    cache_key = _generate_cache_key(new_instance)
    cache.set(cache_key, "1", timeout=None)


def _delete_cache(sender, **kwargs):
    instance = kwargs.get('instance')
    cache_key = _generate_cache_key(instance)
    cache.delete(cache_key)


pre_save.connect(_update_cache, sender=DjangoAdminAccessIPWhitelist)
post_delete.connect(_delete_cache, sender=DjangoAdminAccessIPWhitelist)
