"""
DESCRIPTION：自定义创建用户命令
:useAge:
    1. 创建用户: python manage.py init_superuser
    2. 删除用户: python manage.py init_superuser --delete
:Created by Null.
"""
from django.core.management.base import BaseCommand
from rest_framework_simplejwt.tokens import RefreshToken
from api.models.https import User
from utils.logger import logger


class Command(BaseCommand):
    help = '⚠️Create an superuser with JWT token for testing.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete', action='store_true', help='⚠️Delete poll instead of closing it',
        )

    def handle(self, *args, **kwargs):

        if kwargs['delete']:
            while True:
                username = input("⚠️Please enter the user to be deleted: ")
                try:
                    user = User.objects.filter(username=username).first()
                    user.delete()
                    break
                except (User.DoesNotExist, AttributeError):
                    self.stdout.write(self.style.WARNING('User does not exist! ❌'))
        else:

            username = input("Enter your user name: ")
            password = input("Enter password： ")

            if username and password:
                if not User.objects.filter(email=username).first():
                    superuser = User.objects.create_superuser(
                        email=username, password=password, nickname=username, username=username
                    )
                    refresh = RefreshToken.for_user(superuser)
                    token = str(refresh.access_token)
                    logger.info(f"""

        Your initial superuser has been set for testing, use this user to sign in Django admin:

            Email: {username}
            Password: {password}

        Use this token for jwt testing:

            Authorization: JWT {token}

        """)
