import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.cache import caches


class Command(BaseCommand):

    help = 'Clears cache_id'

    def add_arguments(self, parser):
        parser.add_argument('cache_name', nargs='?', type=str, default='default')

    def handle(self, *args, **options):
        cache_name = options['cache_name']
        try:
            assert settings.CACHES
            caches[cache_name].clear()
            self.stdout.write(self.style.SUCCESS(f'Successfully cleared "{cache_name}" cache'))
        except Exception as err:
            self.stderr.write(self.style.ERROR(f'Failed to clear cache: {err}'))

        logging.info(f"""

        Clearing the application cache succeeded:

            CacheName: {cache_name}

        """)
