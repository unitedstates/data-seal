# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'authapp', b'0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name=b'document',
            name=b'filesize',
        ),
        migrations.RemoveField(
            model_name=b'document',
            name=b'filename',
        ),
        migrations.AlterField(
            model_name=b'document',
            name=b'description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name=b'document',
            name=b'sha256',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name=b'document',
            name=b'sha512',
            field=models.CharField(max_length=512, blank=True),
        ),
        migrations.AlterField(
            model_name=b'document',
            name=b'doc_file',
            field=models.FileField(upload_to=b'server_documents/%Y/%m'),
        ),
        migrations.AlterField(
            model_name=b'document',
            name=b'license',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name=b'document',
            name=b'gpgsig',
            field=models.TextField(blank=True),
        ),
    ]
