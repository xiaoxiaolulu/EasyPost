import os
import subprocess
from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError
)


class Command(BaseCommand):
    help = '⚠️Backing up MySQL Data'

    def add_arguments(self, parser):
        parser.add_argument('--filename', '-f', default='backup.sql', help='⚠️Backup file name')
        parser.add_argument('--compress', '-c', action='store_true', default=False,
                            help='⚠️Whether to compress the backup file')
        parser.add_argument('--encrypt', '-e', action='store_true', default=False,
                            help='⚠️Whether to encrypt the backup file')
        parser.add_argument('--password_env', '-p', default=None, help='⚠️Database password environment variable name')

    def handle(self, *args, **options):
        filename = options.get('filename')
        compress = options.get('compress')
        encrypt = options.get('encrypt')
        password_env = options.get('password_env')

        db_config = settings.DATABASES['default']
        user = db_config['USER']
        host = db_config['HOST']
        port = db_config['PORT']
        db_name = db_config['NAME']

        if password_env:
            password = os.environ.get(password_env)
            if password is None:
                raise CommandError(f"Environment variable '{password_env}' not set. ❌")
        else:
            raise CommandError("Database password not provided. ❌")

        try:
            backup_file = self._backup_db(user, password, host, port, db_name, filename)
            if compress:
                backup_file = self._compress_file(backup_file)
            if encrypt:
                backup_file = self._encrypt_file(backup_file, password)
            self.stdout.write(self.style.SUCCESS(f'Database backup successful: {backup_file} ✅'))
        except Exception as e:
            raise CommandError(f"Error during backup: {e} ❌")

    @staticmethod
    def _backup_db(user, password, host, port, db, filename):
        with open(filename, 'w') as f:
            subprocess.run(['mysqldump', '--user', user, '--password', password, '-h', host, '-P', port, db], stdout=f)
        return filename

    @staticmethod
    def _compress_file(filename):
        compressed_filename = f"{filename}.gz"
        with open(compressed_filename, 'wb') as f_out, open(filename, 'rb') as f_in:
            subprocess.run(['gzip', '-c'], stdin=f_in, stdout=f_out)
        os.remove(filename)  # Optionally remove the uncompressed file
        return compressed_filename

    @staticmethod
    def _encrypt_file(filename, password):
        encrypted_filename = f"{filename}.gpg"
        with open(encrypted_filename, 'wb') as f_out, open(filename, 'rb') as f_in:
            subprocess.run(['gpg', '--yes', '--passphrase', password, '-c'], stdin=f_in, stdout=f_out)
        os.remove(filename)  # Optionally remove the unencrypted file
        return encrypted_filename
