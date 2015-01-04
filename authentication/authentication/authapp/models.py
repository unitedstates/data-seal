from django.db import models
from authentication.authapp.crypto import sign, verify
from tempfile import NamedTemporaryFile
from datetime import datetime
import hashlib
import os
import internetarchive
from django.conf import settings

# Create your models here.
class Document(models.Model):
    doc_file = models.FileField(upload_to="%Y/%m")
    name = models.CharField(max_length=200, blank=True)
    #slug = models.SlugField()
    description = models.TextField(blank=True)
    license = models.TextField(blank=True)

    # filename: os.path.basename(doc_file.name)
    # filesize: doc_file.size

    sha256 = models.CharField(max_length=256, blank=True)
    sha512 = models.CharField(max_length=512, blank=True)
    gpgsig = models.TextField(blank=True)

    uploaded = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
      if self.name:
        return self.name
      else:
        return self.doc_file.url.split('/')[-1]

    def get_ia_url(self):
        url = "https://archive.org/download/"
        url += settings.IA_ITEM + '/'
        url += self.sha256
        url += os.path.splitext(self.doc_file.name)[1]
        return url

    @classmethod
    def sign_this_file(cls, sender, instance, created, **kwargs):
        """
        A callback that gets triggered after a `Document` is saved. Takes the
        file in `Document.doc_file` and runs it through `python-gnupg` (once
        the server is already configured) and saves a PGP signature to the
        `Document.gpgsig` field.
        """
        # Note that we don't care if it's `created` or not. When we upload
        # a new Document, let's sign it so we get a new GPG signature that
        # roughly corresponds with the `updated` timestamp.
        #
        # Use "update" instead of .save() so that we don't infinite-loop
        # and have the .post_save signal send over and over.
        # https://docs.djangoproject.com/en/1.7/ref/models/querysets/#update
        instance.doc_file.file.seek(0)
        Document.objects.filter(id=instance.id).update(gpgsig=sign(instance.doc_file.file.read()))

    @classmethod
    def save_filehashes(cls, sender, instance, created, **kwargs):
        instance.doc_file.file.seek(0)
        sha256 = hashlib.sha256()
        for chunk in iter(lambda: instance.doc_file.file.read(sha256.block_size), b''):
            sha256.update(chunk)
        sha_value = sha256.hexdigest()
        Document.objects.filter(id=instance.id).update(sha256=sha_value)

        instance.doc_file.file.seek(0)
        sha512 = hashlib.sha512()
        for chunk in iter(lambda: instance.doc_file.file.read(sha512.block_size), b''):
            sha512.update(chunk)
        Document.objects.filter(id=instance.id).update(sha512=sha512.hexdigest())
        Document.export_to_ia(instance, sha_value)

    def export_to_ia(self, sha_value, **kwargs):
        """
        Called after a `Document` is signed and the hashes are calculated. Takes the
        file in `Document.doc_file` and uploads it to the internetarchive with the sha256 value as the
        filename.
        """
        item = internetarchive.Item(settings.IA_ITEM)
        md = dict(creator=settings.IA_CREATOR)
        key = sha_value + os.path.splitext(self.doc_file.name)[1]
        item.upload_file(self.doc_file, key=key, metadata=md, access_key=settings.IA_ACCESS_KEY, secret_key=settings.IA_SECRET_KEY)

    def test_user_file(self, uploaded_fp):
        """
        Given a user-uploaded file and this object (self), cryptographically
        compare the user file against the GPG signature for this version
        of the file.

        At this point, we should be pretty sure it's the same file. (Filename, size,
        hash, something that isn't CPU expensive like GPG.)
        """
        # Assume that "uploaded_file" is a file pointer that hasn't
        # been handled yet. Can be in memory or a Django-controlled temp file,
        # we'll write it out to a file that we control just to be sure
        # (so that we can call gpg against this filename).
        # https://docs.djangoproject.com/en/1.7/topics/http/file-uploads/#basic-file-uploads

        # Write the uploaded file to disk, using a `tempfile`
        upload_tmp = NamedTemporaryFile('wb+', delete=False)
        upload_tmpfp = upload_tmp.file
        for chunk in uploaded_fp.chunks():
            upload_tmpfp.write(chunk)
        upload_tmpfp.close()

        # now we can get path to the file we just wrote on disk
        uploaded_file_path = upload_tmp.name

        # Write our gpgsig to a file on disk (<filename>.asc)
        sig_file_path = "%s.asc" % uploaded_file_path
        sigfp = open(sig_file_path, 'wb+')
        sigfp.write(self.gpgsig)
        sigfp.close()

        # do the crypto
        result = verify(uploaded_file_path, sig_file_path)

        # Clean up after ourselves and remove the user's uploaded file.
        if os.path.exists(uploaded_file_path):
            os.unlink(uploaded_file_path)

        # print "User's file matches Agency file %s. File was signed by '%s' (key ID %s) on %s UTC and cryptographically matches the user's file." % (
        #   os.path.basename(self.doc_file.name),
        #   result.username,
        #   result.key_id,
        #   datetime.fromtimestamp(float(result.timestamp)).strftime("%Y-%m-%d %H:%I:%S")
        # )

        # result attrs: username, valid (True or False), timestamp (str of
        # unix timestamp), key_id, and a few others.
        return result

    @staticmethod
    def find_user_file(uploaded_fp):
        """
        Given a user file (via upload), hash the file's data with SHA512
        and then look for a `Document` object that matches that hash.

        We could stand to make this fuzzier / smarter, since we'll be checking
        any matches we get here with GPG.
        """
        h512 = None
        sha512 = hashlib.sha512()
        for chunk in iter(lambda: uploaded_fp.read(sha512.block_size), b''):
            sha512.update(chunk)
        h512 = sha512.hexdigest()

        results = Document.objects.filter(sha512=h512)

        uploaded_fp.seek(0)

        return results

models.signals.post_save.connect(Document.sign_this_file, sender=Document)
models.signals.post_save.connect(Document.save_filehashes, sender=Document)