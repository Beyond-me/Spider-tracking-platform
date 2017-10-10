# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0018_auto_20171009_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articel_id',
            field=models.FloatField(default=1507538069.461534),
        ),
    ]
