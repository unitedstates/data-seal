from django.test import TestCase
from authentication.authapp.models import Document
import subprocess
import unittest
import internetarchive as ia
from django.conf import settings
import os

def have_shasum():
    try:
        subprocess.Popen('shasum')
    except OSError:
        # no shasum
        return False
    return True


def shasum(filename, mode=256):
    p = subprocess.Popen(
        args=['shasum', "-a%d" % mode, filename],
        stdout=subprocess.PIPE
    )
    output = p.stdout.read()

    # output is "hash - filename", so just get the first part
    return output.split(' ')[0]


class DocumentCryptoTestCase(TestCase):
    def test_gpg(self):
        """GPG signature for file validates against itself."""
        doc = Document.objects.get(id=1)
        result = doc.test_user_file(doc.doc_file)
        self.assertTrue(result.valid, "GPG signature validation works.")

    @unittest.skipUnless(have_shasum(), "requires `shasum` installedi")
    def test_sha256_hash(self):
        """SHA256 hash is correctly generated."""
        doc = Document.objects.get(id=1)
        self.assertEqual(
            shasum(doc.doc_file.path, 256),
            doc.sha256,
            "SHA256 hash generation matches output of `shasum -a256`."
        )

    @unittest.skipUnless(have_shasum(), "requires `shasum` installedi")
    def test_sha512_hash(self):
        """SHA512 hash is correctly generated."""
        doc = Document.objects.get(id=1)
        self.assertEqual(
            shasum(doc.doc_file.path, 512),
            doc.sha512,
            "SHA512 hash generation matches output of `shasum -a512`."
        )

    def test_export_to_ia(self):
        doc = Document.objects.get(id=1)
        item = ia.Item(settings.IA_ITEM)
        fname = doc.sha256 + os.path.splitext(doc.doc_file.name)[1]
        i = item.get_file(fname)
        self.assertNotEqual(i, None, "The file is uploaded to the internetarchive")