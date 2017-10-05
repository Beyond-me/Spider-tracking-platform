# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_auto_20171001_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articel_id',
            field=models.FloatField(default=1506873536.877368),
        ),
    ]
