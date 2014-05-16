from django.conf import settings
import gnupg
import os
import subprocess


def gpg_bin():
    """
    If there is a `GNUPG_BINARY` setting, tries to use that as the
    path to the `gpg` or `gpg2` executable. If not, ask the system
    where it is and try to dereference symlinks along the way.
    """
    gpgbin = getattr(settings, "GNUPG_BINARY", None)
    try:
        if not gpgbin:
            gpgbin = subprocess.Popen(
                ['which', 'gpg2'],
                stdout=subprocess.PIPE
            ).stdout.read().strip("\n")
        if not gpgbin:
            gpgbin = subprocess.Popen(
                ['which', 'gpg'],
                stdout=subprocess.PIPE
            ).stdout.read().strip("\n")
    except OSError:
        # Don't have "which" command, so can't ask the OS for the path
        # to the gpg or gpg2 binary
        pass

    if gpgbin:
        # dereference symlinks, since `python-gnupg` can't cope with 'em.
        gpgbin = os.path.realpath(gpgbin)

    if not gpgbin:
        raise Exception("Could not find the `gpg` or `gpg2` executable. Please set GNUPG_BINARY in your local_settings.py file.")

    return gpgbin

def get_gpg(setup_mode=False):
    gpgbin = gpg_bin()
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
