from django.db import models

# Create your models here.
class Document(models.Model):
  name = models.CharField(max_length=200)
  slug = models.SlugField()
  description = models.TextField()
  license = models.TextField()
  doc_file = models.FileField()
  filename = models.CharField(max_length=200)
  filesize = models.BigIntegerField()
  sha256 = models.CharField(max_length=256)
  sha512 = models.CharField(max_length=512)
  gpgsig = models.TextField()
  uploaded = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
