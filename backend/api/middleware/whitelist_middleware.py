import redis
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import MiddlewareNotUsed
from django.utils.deprecation import MiddlewareMixin
from api.models.configuration import (
    DjangoAdminAccessIPWhitelist,
    ADMIN_ACCESS_WHITELIST_PREFIX
)
from utils.logger import logger as logging


class AdminAccessIPWhiteListMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super(AdminAccessIPWhiteListMiddleware, self).__init__(get_response)
        self.ENABLED = getattr(settings, 'ADMIN_ACCESS_WHITELIST_ENABLED', False)
        self.USE_HTTP_X_FORWARDED_FOR = getattr(settings, 'ADMIN_ACCESS_WHITELIST_USE_HTTP_X_FORWARDED_FOR', False)
        self.ADMIN_ACCESS_WHITELIST_MESSAGE = getattr(settings, 'ADMIN_ACCESS_WHITELIST_MESSAGE', 'You are banned.')

        if not self.ENABLED:
            raise MiddlewareNotUsed("❌django-admin-username-whitelist is not enabled via settings.py")

        logging.debug("✳️[django-admin-username-whitelist] status = enabled")

        self.ABUSE_PREFIX = 'DJANGO_ADMIN_ACCESS_WHITELIST_ABUSE:'
        self.WHITELIST_PREFIX = ADMIN_ACCESS_WHITELIST_PREFIX

        for whitelist in DjangoAdminAccessIPWhitelist.objects.all():
            cache_key = self.WHITELIST_PREFIX + whitelist.name
            cache.set(cache_key, "1", timeout=None)

    @staticmethod
    def _get_name(request):
        try:
            name = request.user.nickname
        except AttributeError:
            name = "AnonymousUser"
        return name

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        name = self._get_name(request)
        try:
            if self.is_whitelisted(name):
                return response
            else:
                raise PermissionError('账号不在白名单请联系管理员! ❌')
        except (KeyError, redis.exceptions.AuthorizationError):
            pass
        return response

    def is_whitelisted(self, name):
        is_whitelisted = cache.get(self.WHITELIST_PREFIX + name)

        if is_whitelisted:
            logging.debug("✳️/Admin access IP: " + self.WHITELIST_PREFIX + name)
        return is_whitelisted
