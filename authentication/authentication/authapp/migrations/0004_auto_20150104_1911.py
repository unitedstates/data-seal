# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'authapp', b'0003_auto_20140509_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'document',
            name=b'doc_file',
            field=models.FileField(upload_to=b'%Y/%m'),
        ),
    ]
