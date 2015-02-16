from django.core.management.base import NoArgsCommand, CommandError
from django.utils.crypto import get_random_string

class Command(NoArgsCommand):
    help = 'Prints a SECRET_KEY and GNUPG_PASSPHRASE in local_settings.py.'

    def handle_noargs(self, **options):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        print("SECRET_KEY = '" + get_random_string(50, chars) + "'")
        print("GNUPG_PASSPHRASE = '" + get_random_string(50, chars) + "'")