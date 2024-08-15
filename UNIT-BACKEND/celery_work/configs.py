import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
redis_broker_db = settings.REDIS_DATABASE['CELERY_BROKER']
redis_backend_db = settings.REDIS_DATABASE['CELERY_BACKEND']
broker_url = f'redis://:@{redis_broker_db["HOST"]}:{redis_broker_db["POST"]}/{redis_broker_db["DB"]}'
backend = f'redis://:@{redis_backend_db["HOST"]}:{redis_backend_db["POST"]}/{redis_backend_db["DB"]}'
broker_connection_retry_on_startup = True
