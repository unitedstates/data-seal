from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
import gnupg
import os

class Command(NoArgsCommand):
  help = 'Sets up the initial PGP key for this server.'

  def handle_noargs(self, **options):
    gpgbin = getattr(settings, "GNUPG_BINARY", None)
    gpgdir = os.path.join(settings.BASE_DIR, 'gpgdata')
    # TODO check if gpgdir already exists
    gpg = gnupg.GPG(gpgbin, homedir=gpgdir)
    # TODO get identity from settings
    key_identity = {
      'name_real': 'Authentication.io',
      'name_email': 'test@example.com',
      'expire_date': '2015-01-01',
      'key_type': 'RSA',
      'key_length': 4096,
      'key_usage': '',
      'subkey_type': 'RSA',
      'subkey_length': 4096,
      'subkey_usage': 'sign,auth',
      'passphrase': 'sekrit'
    }
    # TODO check if a private key with same identity (name_real + name_email)
    # already exists
    key_input = gpg.gen_key_input(**key_identity)
    key = gpg.gen_key(key_input)
