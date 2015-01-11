from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from authentication.authapp.crypto import get_gpg
import os


class Command(NoArgsCommand):
    help = 'Sets up the initial PGP key for this server.'

    def handle_noargs(self, **options):
        if settings.GNUPG_BINARY == None:
            print "ERROR: Make sure you set up the local_settings.py first! Your GNUPG_BINARY setting is not set."
            raise SystemExit

        gpg = get_gpg(setup_mode=True)

        # Default settings for key generation
        gpgkey_settings = {
            'key_type': 'RSA',
            'key_length': 4096,
            'key_usage': 'sign,auth',
            'subkey_type': 'RSA',
            'subkey_length': 4096,
            'subkey_usage': 'sign,auth',
        }

        # Fetch key identity information from settings
        gpgkey_settings.update(**settings.GNUPG_IDENTITY_DEFAULTS)

        key_input = gpg.gen_key_input(**gpgkey_settings)
        key = gpg.gen_key(key_input)

        # print "Authentication key generated. Please edit your local_settings.py file"
        # print "and change the `GNUPG_IDENTITY` setting from `None` to:"
        # print
        print 'GNUPG_IDENTITY = "%s"' % str(key)
        # print
        # print "(If you don't have a local_settings.py file, copy local_settings_example.py"
        # print "to local_settings.py and then do the edit there.)"
