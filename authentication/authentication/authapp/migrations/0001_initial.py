# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(max_length=200)),
                (b'slug', models.SlugField()),
                (b'description', models.TextField()),
                (b'license', models.TextField()),
                (b'doc_file', models.FileField(upload_to=b'')),
                (b'filename', models.CharField(max_length=200)),
                (b'filesize', models.BigIntegerField()),
                (b'sha256', models.CharField(max_length=256)),
                (b'sha512', models.CharField(max_length=512)),
                (b'gpgsig', models.TextField()),
                (b'uploaded', models.DateTimeField(auto_now_add=True)),
                (b'updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
