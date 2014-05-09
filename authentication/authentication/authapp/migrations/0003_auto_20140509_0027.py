# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'authapp', b'0002_auto_20140505_0254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name=b'document',
            name=b'slug',
        ),
        migrations.AlterField(
            model_name=b'document',
            name=b'name',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
