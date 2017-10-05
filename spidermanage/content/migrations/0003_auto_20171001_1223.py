# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20170930_1654'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articeltype',
            options={'verbose_name': '\u6587\u7ae0\u7c7b\u578b', 'verbose_name_plural': '\u6587\u7ae0\u7c7b\u578b'},
        ),
        migrations.AlterModelOptions(
            name='tagtype',
            options={'verbose_name': '\u6587\u7ae0\u6807\u7b7e', 'verbose_name_plural': '\u6587\u7ae0\u6807\u7b7e'},
        ),
        migrations.AlterField(
            model_name='article',
            name='articel_id',
            field=models.FloatField(default=1506831828.757639),
        ),
    ]
