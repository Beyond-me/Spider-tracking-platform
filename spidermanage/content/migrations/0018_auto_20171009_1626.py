# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_auto_20171009_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articel_id',
            field=models.FloatField(default=1507537569.128894),
        ),
    ]
