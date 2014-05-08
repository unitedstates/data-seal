from django.conf import settings
import gnupg
import os


def get_gpg(setup_mode=False):
    gpgbin = getattr(settings, "GNUPG_BINARY", None)
    gpgdir = os.path.join(settings.BASE_DIR, 'gpgdata')

    pubring = os.path.join(gpgdir, "pubring.gpg")
    secring = os.path.join(gpgdir, "secring.gpg")

    if setup_mode:
        if os.path.exists(gpgdir) and (os.path.exists(secring) or os.path.exists(pubring)):
            raise Exception("The GnuPG configuration directory (%s) already exists." % gpgdir)

    else:  # not setup mode
        if not getattr(settings, "GNUPG_IDENTITY", None):
            raise Exception("Authentication key not yet configured. Please run 'manage.py gpginit' first.")
        elif not os.path.exists(gpgdir) or not os.path.exists(secring) or not os.path.exists(pubring):
            raise Exception("The GnuPG configuration directory (%s) does not exist." % gpgdir)

    return gnupg.GPG(gpgbin, homedir=gpgdir)


def pubkey():
    if not getattr(settings, "GNUPG_IDENTITY", None):
        raise Exception("Authentication key not yet configured. Please run 'manage.py gpginit' first.")
    return settings.GNUPG_IDENTITY


def sign(data):
    """
    Given a file handle or a string, returns the PGP SIGNATURE for the data,
    as signed by the identity configured in `settings.GNUPG_*`.
    """
    gpg = get_gpg(False)
    return str(gpg.sign(
        data,
        default_key=pubkey(),
        passphrase=settings.GNUPG_PASSPHRASE,
        clearsign=False,
        detach=True,
        binary=False,
        digest_algo="SHA512"
    ))


def verify(data_filename, sig_filename):
    """
    Given a file handle or a string, returns the PGP SIGNATURE for the data,
    as signed by the identity configured in `settings.GNUPG_*`.
    """
    gpg = get_gpg(False)
    val = gpg.verify_file(
        file=data_filename,
        sig_file=sig_filename
    )
    return val
